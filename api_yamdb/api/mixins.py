"""Кастомные настройки вьюсетов приложения API."""
from rest_framework import mixins
from rest_framework import viewsets


class GenreCategoryCreateRetrieve(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Кастомные настройки вьюсета Genre, Category."""
    pass
