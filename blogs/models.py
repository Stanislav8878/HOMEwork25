from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', max_length=220, unique=True)
    content = models.TextField('Содержимое')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    views = models.PositiveIntegerField('Просмотры', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:post_detail', args=[self.pk])
