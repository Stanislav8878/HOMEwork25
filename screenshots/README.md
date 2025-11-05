# Вход в shell
python manage.py shell

# Импорт моделей
from catalog.models import Category, Product

# Создание категорий
cat1 = Category.objects.create(name="Электроника", description="Электронные устройства")
cat2 = Category.objects.create(name="Книги", description="Художественная литература")

# Создание продуктов
product1 = Product.objects.create(name="Смартфон", description="Современный смартфон", category=cat1, price=29999.99)
product2 = Product.objects.create(name="Ноутбук", description="Игровой ноутбук", category=cat1, price=89999.99)
product3 = Product.objects.create(name="Роман", description="Художественный роман", category=cat2, price=599.99)

# Получить все категории
all_categories = Category.objects.all()

# Получить все продукты
all_products = Product.objects.all()

# Найти продукты в категории "Электроника"
electronics = Product.objects.filter(category__name="Электроника")

# Обновить цену продукта
product1.price = 25999.99
product1.save()

# Удалить продукт
product3.delete()