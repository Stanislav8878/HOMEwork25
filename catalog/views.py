from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import ProductForm
from .models import Product, Contact


class HomeView(ListView):
    """
    Общедоступный список товаров.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'



class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр одного товара — только для авторизованных.
    """
    model = Product
    template_name = 'catalog/product_detail.html'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contact_info'] = Contact.objects.all()
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Создание товара — только для авторизованных.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование товара — только для авторизованных.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление товара — только для авторизованных.
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
