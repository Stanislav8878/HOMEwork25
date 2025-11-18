from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Авторизация по email (USERNAME_FIELD = 'email').
    """
    username = None  # убираем username
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # без обязательного username/first_name и т.п.

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email or f'User #{self.pk}'
