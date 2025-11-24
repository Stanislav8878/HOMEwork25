from django.db.models.query import QuerySet
from django.db.utils import InterfaceError


def patch_queryset_exists():
    """
    Патч для QuerySet.exists() на случай бага psycopg3:
    'row must be included between 0 and 0'.
    Если он случается, вместо exists() используем безопасный list(qs[:1]).
    """
    # чтобы не патчить повторно
    if getattr(QuerySet, '_patched_exists', False):
        return

    original_exists = QuerySet.exists

    def exists(self):
        try:
            return original_exists(self)
        except InterfaceError as e:
            if 'row must be included between 0 and 0' in str(e):
                # fallback: проверяем наличие хотя бы одной строки
                return bool(list(self[:1]))
            # если другая ошибка – не глотаем её
            raise

    QuerySet.exists = exists
    QuerySet._patched_exists = True
