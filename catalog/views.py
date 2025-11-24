# catalog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    TemplateView,
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import ProductForm
from .models import Product, Contact, Category
from .services import get_products_by_category


class HomeView(ListView):
    """
    Главная — список последних опубликованных продуктов.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return (
            Product.objects.filter(is_published=True)
            .select_related('category', 'owner')
            .order_by('-created_at')
        )


class ContactsView(TemplateView):
    """
    Страница контактов.
    """
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = Contact.objects.all()
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    """
    Страница одного продукта — кешируем.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Создание продукта — только для авторизованных.
    Владельцем автоматически становится текущий пользователь.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование продукта — только владелец.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied('У вас нет прав для редактирования этого товара.')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление товара — владелец ИЛИ модератор продуктов
    (пользователь с правом catalog.delete_product).
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.has_perm('catalog.delete_product')

    def handle_no_permission(self):
        raise PermissionDenied('У вас нет прав для удаления этого товара.')


def unpublish_product(request, pk):
    """
    Отмена публикации товара.
    Может сделать владелец товара или пользователь с правом can_unpublish_product.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied('Требуется авторизация.')

    product = get_object_or_404(Product, pk=pk)

    if not (
        product.owner == request.user
        or request.user.has_perm('catalog.can_unpublish_product')
    ):
        raise PermissionDenied('У вас нет прав для снятия товара с публикации.')

    product.is_published = False
    product.save(update_fields=['is_published'])

    return redirect(product.get_absolute_url())


class ProductsByCategoryView(ListView):
    """
    Список продуктов по категории, использует сервис с низкоуровневым кешем.
    """
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
