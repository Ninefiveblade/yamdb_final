"""Кастомные настройки вьюсетов приложения API."""
from rest_framework import mixins, viewsets


class GenreCategoryCreateRetrieve(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Кастомные настройки вьюсета Genre, Category."""
    pass
