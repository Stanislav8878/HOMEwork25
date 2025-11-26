import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, MailingAttempt

logger = logging.getLogger('mailings')


def send_mailing(mailing: Mailing):
    """
    Запускает отправку сообщений по указанной рассылке.
    На каждую попытку создаётся запись в MailingAttempt.
    """
    logger.info('Начало рассылки %s', mailing.pk)

    mailing.status = Mailing.STATUS_RUNNING
    mailing.save(update_fields=['status'])

    for client in mailing.clients.all():
        try:
            result = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = MailingAttempt.STATUS_SUCCESS if result else MailingAttempt.STATUS_FAIL
            server_response = f'Send result: {result}'
        except Exception as e:
            status = MailingAttempt.STATUS_FAIL
            server_response = str(e)

        MailingAttempt.objects.create(
            mailing=mailing,
            client=client,
            status=status,
            server_response=server_response,
        )

        logger.info(
            'Попытка отправки: mailing=%s client=%s status=%s',
            mailing.pk,
            client.pk,
            status,
        )

    # если время окончания прошло — считаем рассылку завершённой
    if mailing.end_at <= timezone.now():
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=['status'])
        logger.info('Рассылка %s завершена по времени', mailing.pk)
