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
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        # последние 5 созданных продуктов
        return Product.objects.order_by('-created_at')[:5]


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contact_info'] = Contact.objects.all()
        return ctx


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
