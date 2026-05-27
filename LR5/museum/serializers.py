from rest_framework import serializers

from .models import Exhibition, Hall, Museum, NewsArticle, PromoCode


class MuseumSerializer(serializers.ModelSerializer):
    halls_count = serializers.SerializerMethodField()

    class Meta:
        model = Museum
        fields = ["id", "name", "city", "address", "description", "halls_count"]

    def get_halls_count(self, obj):
        return obj.halls.count()


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ["id", "museum", "number", "name", "floor", "area", "description"]


class ExhibitionSerializer(serializers.ModelSerializer):
    museum_name = serializers.CharField(source="museum.name", read_only=True)

    class Meta:
        model = Exhibition
        fields = ["id", "museum", "museum_name", "title", "description", "start_date", "end_date", "is_active"]


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ["id", "title", "slug", "summary", "body", "published_at"]


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ["id", "code", "description", "discount", "is_active", "valid_from", "valid_to"]
