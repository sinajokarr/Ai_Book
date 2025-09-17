import django_filters as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    price_max =filters.NumberFilter(field_name="unit_price",lookup_expr="gte")
    price_min = filters.NumberFilter(field_name = "unit_price",lookup_expr="lte")
    in_stock =filters.BooleanFilter(field_name="inventory", method="filter_in_stock")
    category = filters.NumberFilter(field_name="category_id")
    
    def filter_in_stock(self,queryset,name,value):
        if value is True :
            return queryset.filter(inventory__gt=0)
        if value is False:
            return queryset.filter(inventory__lte=0)
        return queryset
    
    class Meta:
        model = Product
        fields = ["price_min", "price_max", "in_stock", "category"]