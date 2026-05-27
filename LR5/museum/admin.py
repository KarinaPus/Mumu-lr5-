from django.contrib import admin

from .models import (
    CompanyInfo,
    Exhibition,
    Exhibit,
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


@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "created_at")
    search_fields = ("name", "city")


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("museum", "number", "name", "floor")
    search_fields = ("name", "museum__name")


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "phone")
    search_fields = ("name", "specialization")


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ("title", "hall", "kind", "accession_date")
    list_filter = ("kind",)


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ("title", "museum", "start_date", "end_date")
    filter_horizontal = ("guides",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "museum", "date", "participants")
    filter_horizontal = ("guides",)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "created_at")
    search_fields = ("title", "summary")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "added_at")
    search_fields = ("question", "answer")


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at",)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_active")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "is_active", "valid_from", "valid_to")
    search_fields = ("code",)


@admin.register(TicketPrice)
class TicketPriceAdmin(admin.ModelAdmin):
    list_display = ("day_type", "age_group", "price")


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("visitor", "exhibition", "status", "created_at")
