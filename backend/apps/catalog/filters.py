import django_filters
from .models import Medicine


class MedicineFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method="filter_price", label="Minimum price")
    max_price = django_filters.NumberFilter(method="filter_price", label="Maximum price")
    in_stock = django_filters.BooleanFilter(method="filter_stock")

    class Meta:
        model = Medicine
        fields = ("category", "manufacturer", "dosage_form", "requires_prescription")

    def filter_price(self, queryset, name, value):
        return queryset.filter(inventory_stocks__price__gte=value) if name == "min_price" else queryset.filter(
            inventory_stocks__price__lte=value
        )

    def filter_stock(self, queryset, name, value):
        if value:
            return queryset.filter(inventory_stocks__quantity__gt=0, inventory_stocks__is_available=True).distinct()
        return queryset
