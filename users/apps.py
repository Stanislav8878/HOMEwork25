from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self):
        # Применяем патч для исправления ошибки psycopg3 после инициализации Django
        from config.db_patch import patch_queryset_exists
        patch_queryset_exists()
