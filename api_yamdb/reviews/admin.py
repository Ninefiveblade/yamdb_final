"""Настройка админ панели приложения Reviews"""
from django.contrib import admin

from users.models import YamDBUser
from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    """Настройка отображений для Title"""
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )

    search_fields = ('name',)
    list_filter = ('year',)


class ReviewAdmin(admin.ModelAdmin):
    """Настройка отображений для Review"""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'title_id',
        'score',
        'author'
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(YamDBUser)
