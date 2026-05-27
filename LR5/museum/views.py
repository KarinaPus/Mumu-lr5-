import calendar
import json
import logging
import random
import urllib.request
from datetime import datetime
from datetime import timedelta
from datetime import timezone as dt_timezone

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ExhibitionForm, RegisterForm, ReviewForm, TicketBookingForm, ChildForm
from .models import (
    CompanyInfo,
    Exhibit,
    Exhibition,
    FAQ,
    Guide,
    Hall,
    Museum,
    NewsArticle,
    Profile,
    PromoCode,
    Review,
    Ticket,
    TicketPrice,
    Tour,
    Vacancy,
    Visitor,
)

logger = logging.getLogger("museum")


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def fetch_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.57"
        "&current=temperature_2m,wind_speed_10m&timezone=Europe%2FMoscow"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
        current = data.get("current", {})
        return {
            "temperature": current.get("temperature_2m"),
            "wind": current.get("wind_speed_10m"),
        }
    except Exception as exc:
        logger.warning("Не удалось получить погодные данные: %s", exc)
        return None


def fetch_currency_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
        rates = data.get("rates", {})
        return {
            "usd_to_rub": rates.get("RUB"),
            "usd_to_eur": rates.get("EUR"),
        }
    except Exception as exc:
        logger.warning("Не удалось получить курс валют: %s", exc)
        return None


def home_view(request):
    now = timezone.localtime()
    news_qs = NewsArticle.objects.filter(published_at__lte=now).order_by("-published_at")
    news_of_the_day = random.choice(list(news_qs[:5])) if news_qs.exists() else None
    company_info = CompanyInfo.objects.order_by("-updated_at").first()
    weather = fetch_weather_data()
    currency = fetch_currency_rate()
    latest = Exhibition.objects.order_by("-start_date")[:5]
    featured_exhibits = (
        Exhibit.objects.select_related("hall")
        .order_by("-accession_date")[:6]
    )

    context = {
        "latest_exhibitions": latest,
        "featured_exhibits": featured_exhibits,
        "news_of_the_day": news_of_the_day,
        "company_info": company_info,
        "weather": weather,
        "currency": currency,
        "current_date": now.strftime("%d/%m/%Y"),
        "current_time": now.strftime("%H:%M"),
        "timezone_name": timezone.get_current_timezone_name(),
        "utc_now": timezone.now().astimezone(dt_timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        "calendar_text": calendar.month(now.year, now.month),
    }
    return render(request, "museum/home.html", context)


class ExhibitionListView(ListView):
    model = Exhibition
    template_name = "museum/exhibition_list.html"
    context_object_name = "exhibitions"
    paginate_by = 5

    def get_queryset(self):
        qs = Exhibition.objects.select_related("museum").prefetch_related("guides")
        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort", "-start_date")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if sort not in {"title", "-start_date", "start_date"}:
            sort = "-start_date"
        return qs.order_by(sort)


class ExhibitionDetailView(DetailView):
    model = Exhibition
    template_name = "museum/exhibition_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["can_book"] = self.request.user.is_authenticated
        return ctx


class ExhibitionCreateView(SuperuserRequiredMixin, CreateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = "museum/exhibition_form.html"
    success_url = reverse_lazy("museum:exhibition-list")


class ExhibitionUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = "museum/exhibition_form.html"
    success_url = reverse_lazy("museum:exhibition-list")


class ExhibitionDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Exhibition
    template_name = "museum/exhibition_confirm_delete.html"
    success_url = reverse_lazy("museum:exhibition-list")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "museum/register.html"
    success_url = reverse_lazy("museum:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        Visitor.objects.get_or_create(user=self.object)
        Profile.objects.get_or_create(user=self.object, defaults={"role": "visitor"})
        login(self.request, self.object)
        return response


@login_required
def booking_view(request):
    visitor = getattr(request.user, 'visitor', None)
    
    if not visitor:
        return HttpResponseForbidden("Профиль не найден.")
    
    # Проверка на 18+ ТОЛЬКО для выставок с рейтингом 18+
    exhibitions = Exhibition.objects.filter(is_active=True)
    form = TicketBookingForm(request.POST or None, exhibitions=exhibitions, user=request.user)

    if request.method == "POST" and form.is_valid():
        exhibition = form.cleaned_data["exhibition"]
        visitor_type = form.cleaned_data["visitor_type"]
        quantity = form.cleaned_data["quantity"]
        child = form.cleaned_data.get("child")
        
        if exhibition.is_adult_only and visitor_type == 'child':
            form.add_error(None, "Данная выставка предназначена только для посетителей 18+")
            return render(request, "museum/booking.html", {"form": form})
        # Расчет цены (льготная для детей)
        from .models import TicketPrice
        from django.utils import timezone
        
        day_type = 'weekday' if timezone.localtime().weekday() < 5 else 'weekend'
        age_group = 'child' if visitor_type == 'child' else 'adult'
        
        try:
            price = TicketPrice.objects.get(day_type=day_type, age_group=age_group)
            ticket_price = price.price
        except TicketPrice.DoesNotExist:
            ticket_price = 0
        
        # Создаем билет(ы)
        for _ in range(quantity):
            ticket = Ticket.objects.create(
                visitor=visitor,
                exhibition=exhibition,
                status="booked",
                visitor_type=visitor_type,
                price=ticket_price
            )
            
            # Если билет для ребенка, связываем
            if visitor_type == 'child' and form.cleaned_data.get('child'):
                ticket.child_visitor = form.cleaned_data['child']
                ticket.save()
        
        logger.info("Пользователь %s забронировал %d билет(ов) на %s (тип: %s)", 
                   request.user.username, quantity, exhibition.title, visitor_type)
        return redirect("museum:cabinet")

    return render(request, "museum/booking.html", {"form": form})


@login_required
def cabinet_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={"role": "visitor"})
    visitor, _ = Visitor.objects.get_or_create(user=request.user)
    tickets = Ticket.objects.filter(visitor=visitor).select_related("exhibition")
    reviews = Review.objects.filter(visitor=visitor).order_by("-created_at")
    active_promocodes = PromoCode.objects.filter(is_active=True).order_by("-created_at")

    guide = None
    assigned_exhibits = Exhibit.objects.none()
    guided_tours = Tour.objects.none()

    if profile.role == "employee":
        full_name = request.user.get_full_name().strip()
        guide_name = full_name or request.user.username
        guide = Guide.objects.filter(name__iexact=guide_name).first()
        if guide is not None:
            assigned_exhibits = (
                Exhibit.objects.filter(assigned_guide=guide)
                .select_related("hall")
                .order_by("-accession_date")
            )
            guided_tours = Tour.objects.filter(guides=guide).order_by("date")

    return render(
        request,
        "museum/cabinet.html",
        {
            "tickets": tickets,
            "reviews": reviews,
            "profile": profile,
            "active_promocodes": active_promocodes,
            "guide": guide,
            "assigned_exhibits": assigned_exhibits,
            "guided_tours": guided_tours,
        },
    )


def about_view(request):
    company_info = CompanyInfo.objects.order_by("-updated_at").first()
    halls = Hall.objects.select_related("museum").order_by("museum__name", "number")
    return render(request, "museum/about.html", {"company_info": company_info, "halls": halls})


def news_list_view(request):
    search = request.GET.get("search", "")
    qs = NewsArticle.objects.filter(published_at__lte=timezone.now()).order_by("-published_at")
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(summary__icontains=search))
    return render(request, "museum/news_list.html", {"news": qs, "search": search})


def news_detail_view(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    return render(request, "museum/news_detail.html", {"article": article})


def faq_view(request):
    search = request.GET.get("search", "")
    qs = FAQ.objects.all().order_by("-added_at")
    if search:
        qs = qs.filter(Q(question__icontains=search) | Q(answer__icontains=search))
    return render(request, "museum/faq.html", {"faqs": qs, "search": search})


def contacts_view(request):
    guides = Guide.objects.all().order_by("name")
    museum = Museum.objects.first()
    return render(request, "museum/contacts.html", {"guides": guides, "museum": museum})


def privacy_view(request):
    return render(request, "museum/privacy.html")


def vacancies_view(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by("-published_at")
    return render(request, "museum/vacancies.html", {"vacancies": vacancies})


def reviews_view(request):
    reviews = Review.objects.order_by("-created_at")[:20]
    return render(request, "museum/reviews.html", {"reviews": reviews})


@login_required
def review_create_view(request):
    form = ReviewForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.visitor = getattr(request.user, "visitor", None)
        review.author_name = request.user.get_full_name() or request.user.username
        review.save()
        logger.info("Пользователь %s оставил отзыв", request.user.username)
        return redirect("museum:reviews")
    return render(request, "museum/review_form.html", {"form": form})


def promocodes_view(request):
    active = PromoCode.objects.filter(is_active=True).order_by("-created_at")
    archive = PromoCode.objects.filter(is_active=False).order_by("-created_at")
    return render(request, "museum/promocodes.html", {"active_promocodes": active, "archive_promocodes": archive})


def ticket_prices_view(request):
    prices = TicketPrice.objects.order_by("day_type", "age_group")
    return render(request, "museum/tickets.html", {"prices": prices})


@login_required
def stats_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступно только администраторам")

    average_rating = Review.objects.aggregate(avg=Avg("rating"))
    hall_counts = list(
        Hall.objects.annotate(exhibit_count=Count("exhibits"))
        .order_by("-exhibit_count", "name")
        .values_list("name", "exhibit_count")
    )
    kind_counts = list(
        Exhibit.objects.values("kind")
        .annotate(count=Count("id"))
        .order_by("-count", "kind")
    )

    hall_chart = []
    for index, (name, count) in enumerate(hall_counts):
        bar_height = max(24, count * 18)
        hall_chart.append(
            {
                "label": name,
                "count": count,
                "x": 60 + index * 70,
                "bar_height": bar_height,
                "bar_y": 220 - bar_height,
                "value_y": 200 - bar_height,
                "label_y": 240,
            }
        )

    kind_chart = []
    for index, item in enumerate(kind_counts):
        count = item["count"]
        bar_height = max(24, count * 18)
        kind_chart.append(
            {
                "label": item["kind"],
                "count": count,
                "x": 60 + index * 70,
                "bar_height": bar_height,
                "bar_y": 220 - bar_height,
                "value_y": 200 - bar_height,
                "label_y": 240,
            }
        )

    season = request.GET.get("season", "")
    floor_value = request.GET.get("floor", "")
    date_value = request.GET.get("date", "")

    floor_number = None
    if floor_value.isdigit():
        floor_number = int(floor_value)

    selected_date = None
    if date_value:
        try:
            selected_date = datetime.fromisoformat(date_value).date()
        except ValueError:
            selected_date = None

    half_year_ago = timezone.now().date() - timedelta(days=180)
    recent_exhibits = (
        Exhibit.objects.select_related("hall", "assigned_guide")
        .filter(accession_date__gte=half_year_ago)
        .order_by("-accession_date")
    )

    guides = Guide.objects.select_related("hall").all()
    if floor_number is not None:
        guides = guides.filter(hall__floor=floor_number)

    tours = Tour.objects.select_related("museum").all()
    if season:
        season_months = {
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11],
            "winter": [12, 1, 2],
        }
        months = season_months.get(season, [])
        if months:
            if season == "winter":
                tours = tours.filter(Q(date__month__in=[12, 1, 2]))
            else:
                tours = tours.filter(date__month__in=months)

    hall_counts_after_date = []
    if selected_date:
        hall_counts_after_date = list(
            Hall.objects.annotate(
                exhibit_count=Count("exhibits", filter=Q(exhibits__accession_date__gte=selected_date))
            )
            .order_by("number")
            .values_list("number", "name", "floor", "area", "exhibit_count")
        )

    stats = {
        "museums": Museum.objects.count(),
        "halls": Hall.objects.count(),
        "exhibits": Exhibit.objects.count(),
        "exhibitions": Exhibition.objects.count(),
        "tours": Tour.objects.count(),
        "tickets": Ticket.objects.count(),
        "guided_exhibitions": Exhibition.objects.filter(guides__isnull=False).distinct().count(),
        "active_exhibitions": Exhibition.objects.filter(is_active=True).count(),
        "news": NewsArticle.objects.count(),
        "active_promocodes": PromoCode.objects.filter(is_active=True).count(),
        "reviews": Review.objects.count(),
        "average_rating": average_rating["avg"] or 0,
        "hall_counts": hall_chart,
        "kind_counts": kind_chart,
        "halls_list": Hall.objects.order_by("number"),
        "recent_exhibits": recent_exhibits,
        "guides": guides,
        "tours": tours,
        "hall_counts_after_date": hall_counts_after_date,
        "selected_floor": floor_value,
        "selected_season": season,
        "selected_date": date_value,
        "selected_floor_number": floor_number,
        "season_tour_count": tours.count(),
        "recent_exhibit_count": recent_exhibits.count(),
    }
    return render(request, "museum/stats.html", stats)
@login_required
def add_child_view(request):
    """Добавление ребенка для льготных билетов"""
    visitor = getattr(request.user, 'visitor', None)
    
    if not visitor:
        return HttpResponseForbidden("Профиль не найден.")
    
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            # Создаем ребенка, привязывая к текущему пользователю
            child = form.save(commit=False)
            child.parent = visitor
            child.save()
            
            # Логируем
            import logging
            logger = logging.getLogger("museum")
            logger.info(f"Пользователь {request.user.username} добавил ребенка {child.first_name}")
            
            return redirect('museum:cabinet')
        else:
            # Если форма не валидна, покажем ошибки
            return render(request, 'museum/add_child.html', {'form': form})
    else:
        form = ChildForm()
    
    return render(request, 'museum/add_child.html', {'form': form})