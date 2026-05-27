from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
    Child,
)
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')



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
    list_display = ('user', 'phone', 'birth_date', 'is_parent', 'age')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('is_parent',)
    readonly_fields = ('age',)
    
    def age(self, obj):
        return obj.age
    age.short_description = "Возраст"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("visitor", "exhibition", "status", "created_at")

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'parent', 'birth_date', 'age')
    list_filter = ('parent',)
    search_fields = ('first_name', 'last_name', 'parent__user__username')
    
    def age(self, obj):
        return obj.age
    age.short_description = "Возраст"