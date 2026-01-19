# catalog/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField('Наименование', max_length=200)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField(
        'Изображение',
        upload_to='products/',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='products',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    # Статус публикации — по умолчанию НЕ опубликован
    is_published = models.BooleanField('Опубликовано', default=False)

    # Владелец продукта
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Владелец',
        related_name='products',
        on_delete=models.CASCADE,
        blank=True,
        null=True,  # оставляем nullable, чтобы не падали фикстуры и старая команда load_products
    )

    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        # Кастомное право для модераторов продуктов
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.pk])


class Contact(models.Model):
    country = models.CharField(max_length=100, verbose_name='Страна')
    inn = models.CharField(max_length=20, verbose_name='ИНН')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self) -> str:
        return f"{self.country} - {self.address}"
