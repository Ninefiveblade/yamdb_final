"""Кастомные настройки пагинации приложения API."""
from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class ApiPagination(PageNumberPagination):
    """Кастомный класс пагинации.
    page_size - страницы по умолчанию.
    """
    page_size = settings.PAGE_SIZE
