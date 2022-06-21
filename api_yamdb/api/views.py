"""Вью классы приложения API."""
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews import models
from users.models import YamDBUser
from . import serializers
from .filters import TitleFilter
from .mixins import GenreCategoryCreateRetrieve
from .pagination import ApiPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, IsStaffOrOwner


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений.
    get_queryset - кастомный queryset."""
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = ApiPagination
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов.
    perform_create - опции создания обекта
    get_queryset - кастомный queryset.
    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (IsStaffOrOwner,)
    pagination_class = ApiPagination

    def perform_create(self, serializer):
        title = get_object_or_404(
            models.Title, id=self.kwargs.get("title_id")
        )
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_queryset(self):
        comments = models.Review.objects.filter(
            title_id=self.kwargs.get("title_id")
        )
        return comments


class CategoryViewSet(GenreCategoryCreateRetrieve):
    """Вьюсет категорий."""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = ApiPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(GenreCategoryCreateRetrieve):
    """Вьюсет Жанров."""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = ApiPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев.
    perform_create - опции создания обекта
    get_queryset - кастомный queryset.
    """
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsStaffOrOwner,)
    pagination_class = ApiPagination

    def perform_create(self, serializer):
        review = get_object_or_404(
            models.Review, id=self.kwargs.get("review_id")
        )
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        comments = models.Comment.objects.filter(
            review_id=self.kwargs.get("review_id")
        )
        return comments


@permission_classes((AllowAny,))
@api_view(['POST'])
def register(request):
    """Регистрация пользователя на платформе."""
    serializer = serializers.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = {
        "username": serializer.data.get('username'),
        "email": serializer.data.get('email')
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token_view(request):
    """Получение токена для user."""
    serializer = serializers.ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(YamDBUser, username=username)
    token = serializer.validated_data.get('confirmation_code')
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        token = RefreshToken.for_user(user)
        access_token = {
            "token": str(token.access_token)
        }
        return Response(access_token, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.mixins.CreateModelMixin,
                  viewsets.mixins.DestroyModelMixin,
                  viewsets.mixins.UpdateModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет пользователей.
    get_serializer_class -
    Выбор сериализатора в зависимости
    от роли пользователя.
    Метод me - метод способ реализации
    current user для url.
    """
    queryset = YamDBUser.objects.all()
    permission_classes = (IsAdmin, )
    pagination_class = ApiPagination
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return serializers.AdminSerializer
        return serializers.UserSerializer

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(partial=True, role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
