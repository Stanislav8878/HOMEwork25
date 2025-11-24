from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product
from blogs.models import Post


class Command(BaseCommand):
    help = "Создаёт группы 'Модератор продуктов' и 'Контент-менеджер' с нужными правами"

    def handle(self, *args, **options):
        # ContentType для моделей
        product_ct = ContentType.objects.get_for_model(Product)
        post_ct = ContentType.objects.get_for_model(Post)

        # --- Группа "Модератор продуктов" ---
        product_moderator, _ = Group.objects.get_or_create(name='Модератор продуктов')

        can_unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Can unpublish product',
            content_type=product_ct,
        )
        delete_product_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_ct,
        )

        product_moderator.permissions.set([can_unpublish_perm, delete_product_perm])

        # --- Группа "Контент-менеджер" ---
        content_manager, _ = Group.objects.get_or_create(name='Контент-менеджер')

        blog_perms = Permission.objects.filter(
            content_type=post_ct,
            codename__in=['add_post', 'change_post', 'delete_post'],
        )
        content_manager.permissions.set(blog_perms)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы/обновлены.'))
