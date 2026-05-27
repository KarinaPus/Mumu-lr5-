from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Exhibition, Museum, NewsArticle, PromoCode
from .serializers import ExhibitionSerializer, MuseumSerializer, NewsArticleSerializer, PromoCodeSerializer


class MuseumViewSet(viewsets.ModelViewSet):
    queryset = Museum.objects.all().order_by("name")
    serializer_class = MuseumSerializer
    permission_classes = [IsAuthenticated]


class ExhibitionViewSet(viewsets.ModelViewSet):
    queryset = Exhibition.objects.select_related("museum").all().order_by("-start_date")
    serializer_class = ExhibitionSerializer
    permission_classes = [IsAuthenticated]


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by("-published_at")
    serializer_class = NewsArticleSerializer
    permission_classes = [IsAuthenticated]


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all().order_by("-created_at")
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]
