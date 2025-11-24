from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id, cache_timeout=60 * 5):
    """
    Возвращает список всех опубликованных продуктов в указанной категории
    с низкоуровневым кешированием.
    """
    cache_key = f'products_by_category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True,
            ).select_related('category', 'owner')
        )
        cache.set(cache_key, products, cache_timeout)

    return products
