from django.conf import settings
from django.db import models


class Client(models.Model):
    email = models.EmailField('Email', unique=True)
    full_name = models.CharField('Ф.И.О.', max_length=255)
    comment = models.TextField('Комментарий', blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Владелец',
    )

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        permissions = [
            ('view_all_clients', 'Может смотреть всех клиентов (менеджер)'),
        ]

    def __str__(self):
        return f'{self.full_name} <{self.email}>'


class Message(models.Model):
    subject = models.CharField('Тема письма', max_length=255)
    body = models.TextField('Тело письма')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Владелец',
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ('view_all_messages', 'Может смотреть все сообщения (менеджер)'),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CREATED = 'created'
    STATUS_RUNNING = 'running'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_RUNNING, 'Запущена'),
        (STATUS_FINISHED, 'Завершена'),
    ]

    start_at = models.DateTimeField('Дата и время первой отправки')
    end_at = models.DateTimeField('Дата и время окончания отправки')
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Сообщение',
    )
    clients = models.ManyToManyField(
        Client,
        related_name='mailings',
        verbose_name='Получатели',
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Владелец',
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('view_all_mailings', 'Может смотреть все рассылки (менеджер)'),
            ('disable_mailings', 'Может отключать рассылки'),
        ]

    def __str__(self):
        return f'Рассылка #{self.pk} ({self.get_status_display()})'


class MailingAttempt(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAIL, 'Не успешно'),
    ]

    attempted_at = models.DateTimeField('Дата и время попытки', auto_now_add=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField('Ответ почтового сервера', blank=True)

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Получатель',
    )

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'

    def __str__(self):
        return f'Попытка #{self.pk} ({self.get_status_display()})'
