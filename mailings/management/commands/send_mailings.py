from django.core.management.base import BaseCommand
from django.utils import timezone

from mailings.models import Mailing
from mailings.services import send_mailing


class Command(BaseCommand):
    help = 'Отправка активных рассылок'

    def handle(self, *args, **options):
        now = timezone.now()
        qs = Mailing.objects.filter(
            status__in=[Mailing.STATUS_CREATED, Mailing.STATUS_RUNNING],
            start_at__lte=now,
            end_at__gte=now,
        )

        if not qs.exists():
            self.stdout.write('Нет рассылок для отправки.')
            return

        for mailing in qs:
            self.stdout.write(self.style.SUCCESS(f'Отправка рассылки {mailing.pk}'))
            send_mailing(mailing)
