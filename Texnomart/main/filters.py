import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max', 'is_liked']


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['title']
