"""Модели приложения users"""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models


class YamDBUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    """Кастомная модель User."""
    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]

    role = models.CharField(max_length=100, choices=ROLES, default=USER)
    bio = models.CharField(max_length=100, null=True, blank=True)

    def send_confirmation_code(self):
        """Подключение отправки почтой."""
        subject = 'Email Verification'
        verification_token = default_token_generator.make_token(self)
        send_mail(
            subject=subject,
            message=f'your confirmation code is {verification_token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(self.email,)
        )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == YamDBUser.ADMIN

    @property
    def is_moderator(self):
        return self.role == YamDBUser.MODERATOR

    @property
    def is_user(self):
        return self.role == YamDBUser.USER

    class Meta:
        ordering = ['-username']
