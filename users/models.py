from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.utils import InterfaceError
from django.core.exceptions import ValidationError


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
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def validate_unique(self, exclude=None):
        """
        Переопределяем validate_unique для обработки ошибки psycopg3.
        """
        try:
            super().validate_unique(exclude=exclude)
        except InterfaceError as e:
            if 'row must be included between 0 and 0' in str(e):
                errors = {}

                if 'email' not in (exclude or []):
                    if self.email:
                        try:
                            qs = User.objects.filter(email=self.email)
                            if self.pk:
                                qs = qs.exclude(pk=self.pk)
                            # list(qs[:1]) вместо exists()
                            if list(qs[:1]):
                                errors['email'] = ['Пользователь с таким email уже существует.']
                        except InterfaceError:
                            # если и тут что-то упало — не душим пользователя
                            pass

                if errors:
                    raise ValidationError(errors)
            else:
                raise

    def __str__(self):
        return self.email or f'User #{self.pk}'
