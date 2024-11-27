from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from goods.models import Product
from goods.utils import ProductFilter


class MainView(TemplateView):
    template_name = 'goods/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Головна'
        return context


class CatalogView(ListView):
    paginate_by = 4
    template_name = 'goods/catalog.html'
    model = Product
    context_object_name = 'products'
    filter = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True).order_by('-created_at')
        filtered_queryset = self.filter(self.request.GET, queryset)
        return filtered_queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['filter'] = self.filter
        return context

class ProductView(DetailView):
    template_name = 'goods/product.html'
    model = Product
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs['product_slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
