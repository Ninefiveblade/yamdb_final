"""Сериализаторы приложения API."""
from django.db import transaction
from rest_framework import serializers

from reviews import models
from users.models import YamDBUser


class CustomSlugRelatedField(serializers.SlugRelatedField):
    """Кастомное поле сериализатора."""
    def to_representation(self, value):
        return {"name": value.name, "slug": value.slug}


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = models.Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = models.Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    rating = serializers.SerializerMethodField()
    genre = CustomSlugRelatedField(
        slug_field='slug',
        queryset=models.Genre.objects.all(),
        many=True
    )
    category = CustomSlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        result = []
        for scores in models.Review.objects.filter(title=obj.id):
            result.append(scores.score)
        if len(result) != 0:
            total_result = sum(result) / len(result)
            return round(total_result, 2)
        return None


class ReviewSerialier(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    """Сериализатор отзывов."""
    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def create(self, validated_data):
        current_review = models.Review.objects.filter(
            author=validated_data.get('author'),
            title_id=validated_data.get('title')
        )
        if current_review.exists():
            raise serializers.ValidationError(
                "You can't add more than one review on this title"
            )
        return models.Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментов."""
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ConfirmCodeSerializer(serializers.ModelSerializer):
    """Сериализатор users.
    username, confirmation_code - добавленные поля.
    """
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = YamDBUser
        fields = (
            'username', 'confirmation_code'
        )


class BaseUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = YamDBUser
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        )

    def validate(self, data):
        email = self.initial_data.get('email')
        username = self.initial_data.get('username')
        if YamDBUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('email must be unique!')
        if YamDBUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('username must be unique!')
        if username == 'me':
            raise serializers.ValidationError(
                'this username is already registered'
            )
        return data


class AdminSerializer(BaseUserSerializer):
    """Admin сериалайзер, необходим для добавления пользователей
    администратором без отправления письма.
    Наследуется от BaseUserSerializer
    """


class UserSerializer(BaseUserSerializer):

    @transaction.atomic
    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.send_confirmation_code()
        return user
