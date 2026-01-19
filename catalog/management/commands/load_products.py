from django.core.management.base import BaseCommand
from catalog.models import Category, Product, Contact


class Command(BaseCommand):
    help = 'Load test products from fixtures'

    def handle(self, *args, **options):
        # Удаляем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()

        self.stdout.write('Deleted all existing products, categories and contacts')

        # Создаем тестовые категории
        categories_data = [
            {'name': 'Электроника', 'description': 'Электронные устройства'},
            {'name': 'Книги', 'description': 'Художественная литература'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'Created category: {category.name}')

        # Создаем тестовые продукты
        products_data = [
            {'name': 'Смартфон', 'description': 'Современный смартфон', 'category': categories['Электроника'],
             'price': 29999.99},
            {'name': 'Ноутбук', 'description': 'Игровой ноутбук', 'category': categories['Электроника'],
             'price': 89999.99},
            {'name': 'Наушники', 'description': 'Беспроводные наушники', 'category': categories['Электроника'],
             'price': 7999.99},
            {'name': 'Роман', 'description': 'Художественный роман', 'category': categories['Книги'], 'price': 599.99},
            {'name': 'Учебник', 'description': 'Учебное пособие', 'category': categories['Книги'], 'price': 1299.99},
            {'name': 'Футболка', 'description': 'Хлопковая футболка', 'category': categories['Одежда'],
             'price': 1499.99},
            {'name': 'Джинсы', 'description': 'Классические джинсы', 'category': categories['Одежда'],
             'price': 3499.99},
        ]

        for product_data in products_data:
            product = Product.objects.create(**product_data)
            self.stdout.write(f'Created product: {product.name} - {product.price}')

        # Создаем контактную информацию
        contact_data = {
            'country': 'USA',
            'inn': '91-1144442',
            'address': 'Redmond, WA, 98052-6399',
            'phone': '+1-425-882-8080',
            'email': 'info@skystore.com'
        }
        contact = Contact.objects.create(**contact_data)
        self.stdout.write(f'Created contact: {contact.country}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data'))
