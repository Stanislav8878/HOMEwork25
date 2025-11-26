from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт/обновляет группу "Менеджеры" для сервиса рассылок'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        perms_codenames = [
            'view_all_clients',
            'view_all_messages',
            'view_all_mailings',
            'disable_mailings',
        ]

        perms = Permission.objects.filter(codename__in=perms_codenames)
        group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" настроена'))
