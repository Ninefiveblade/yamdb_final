"""Кастомные фильтры приложения API"""
import django_filters as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Кастомный фильтр для вьюсета Title
    поиск по полям genre, category."""
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')
