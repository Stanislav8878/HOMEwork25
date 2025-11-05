from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from .models import Product, Contact
from .forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        # сохраняем твою бизнес-логику с '-created_at'
        return Product.objects.all().order_by('-created_at')[:5]

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
