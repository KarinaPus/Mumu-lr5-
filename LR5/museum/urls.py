from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (
    ExhibitionCreateView,
    ExhibitionDeleteView,
    ExhibitionDetailView,
    ExhibitionListView,
    ExhibitionUpdateView,
    RegisterView,
    about_view,
    booking_view,
    cabinet_view,
    contacts_view,
    faq_view,
    home_view,
    news_detail_view,
    news_list_view,
    privacy_view,
    promocodes_view,
    review_create_view,
    reviews_view,
    stats_view,
    ticket_prices_view,
    vacancies_view,
)
from .views_api import ExhibitionViewSet, MuseumViewSet, NewsArticleViewSet, PromoCodeViewSet

app_name = "museum"

router = DefaultRouter()
router.register(r"museums", MuseumViewSet, basename="museum-api")
router.register(r"exhibitions", ExhibitionViewSet, basename="exhibition-api")
router.register(r"news", NewsArticleViewSet, basename="news-api")
router.register(r"promocodes", PromoCodeViewSet, basename="promocodes-api")

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("news/", news_list_view, name="news-list"),
    re_path(r"^news/(?P<slug>[A-Za-z0-9_-]+)/$", news_detail_view, name="news-detail"),
    path("faq/", faq_view, name="faq"),
    path("contacts/", contacts_view, name="contacts"),
    path("privacy/", privacy_view, name="privacy"),
    path("vacancies/", vacancies_view, name="vacancies"),
    path("reviews/", reviews_view, name="reviews"),
    path("reviews/add/", review_create_view, name="review-create"),
    path("promocodes/", promocodes_view, name="promocodes"),
    path("tickets/", ticket_prices_view, name="tickets"),
    path("cabinet/", cabinet_view, name="cabinet"),
    path("exhibitions/", ExhibitionListView.as_view(), name="exhibition-list"),
    path("exhibitions/<int:pk>/", ExhibitionDetailView.as_view(), name="exhibition-detail"),
    path("exhibitions/create/", ExhibitionCreateView.as_view(), name="exhibition-create"),
    path("exhibitions/<int:pk>/edit/", ExhibitionUpdateView.as_view(), name="exhibition-edit"),
    path("exhibitions/<int:pk>/delete/", ExhibitionDeleteView.as_view(), name="exhibition-delete"),
    path("booking/", booking_view, name="booking"),
    path("stats/", stats_view, name="stats"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="museum/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/auth/token/", obtain_auth_token, name="api-token"),
    path("api/", include(router.urls)),
]
