from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.utils import InterfaceError
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.
    Создаёт пользователей и суперпользователей по email (без username).
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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
    REQUIRED_FIELDS = []  # важно: пустой список

    # 👇 привязываем кастомный менеджер
    objects = UserManager()

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
