from django.contrib import admin
from .models import Category, Product, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('price',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('country', 'inn', 'address', 'phone', 'email')
    search_fields = ('country', 'address')
