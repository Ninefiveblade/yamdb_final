"""Роутинг приложения API."""
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'^v1/users', views.UserViewSet, basename='users')
router.register(r'^v1/genres', views.GenreViewSet, basename='genres')
router.register(r'v1/categories', views.CategoryViewSet, basename='categories')
router.register(r'v1/titles', views.TitleViewSet, basename='titles')
router.register(
    r'^v1/titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/token/', views.obtain_token_view),
    path('v1/auth/signup/', views.register)
]
