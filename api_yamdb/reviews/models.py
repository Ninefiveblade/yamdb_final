"""Модели приложения reviews."""
from django.db import models
from django.db.models.deletion import SET_NULL
from users.models import YamDBUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now


class Title(models.Model):
    """Модель произведений
    Связи без категорий без удаления
    Произведения.
    """
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField(
        help_text='Год',
        db_index=True,
        validators=[
            MaxValueValidator(now().year),
        ],
        blank=True
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=SET_NULL,
        related_name='categories',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='genre_title',
        blank=True,
        verbose_name='Жанры'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles_review',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        help_text='Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    author = models.ForeignKey(
        YamDBUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            )
        ]


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    "Модель жанров."
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Comment(models.Model):
    """Модель коментариев."""
    text = models.CharField('Текст комментария', max_length=256)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        YamDBUser,
        on_delete=models.CASCADE,
        related_name='comment_autor'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments_review'
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']
