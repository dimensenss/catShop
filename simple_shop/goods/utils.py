import django_filters
from django import forms

from django.db.models import Q

from goods.models import Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='name_desc_filter', label='Назва складається з')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Ціна від:')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Ціна до:')
    is_free = django_filters.BooleanFilter(method='is_free_filter', widget=forms.CheckboxInput,
                                           label='Віддають в добрі руки')

    def name_desc_filter(self, queryset, name, value):
        if value.isdigit() and len(value) <= 5:
            return queryset.filter(id=value)
        value = value.lower()
        query = Q(title__icontains=value) | Q(description__icontains=value)
        return queryset.filter(query).distinct()

    def is_free_filter(self, queryset, name, value):
        if value:
            return queryset.filter(price=0)
        return queryset

    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
        ),
        field_labels={
            'price': 'Від дешевих до дорогих',
            '-price': 'Від дорогих до дешевих',
        },
        empty_label=None,
    )

    class Meta:
        model = Product
        fields = []