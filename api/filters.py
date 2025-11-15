"""
Filters for the API app.
"""

import django_filters

from .models import Person, Product


class PersonFilter(django_filters.FilterSet):
    """Filter for Person list view."""

    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    ordering = django_filters.OrderingFilter(
        fields=(("created_at", "created_at"),),
        field_labels={
            "created_at": "Fecha de creación",
        },
    )

    class Meta:
        model = Person
        fields = ["email", "last_name"]


class ProductFilter(django_filters.FilterSet):
    """Filter for Product list view."""

    sku = django_filters.CharFilter(field_name="sku", lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    q = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Search by name"
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("price", "price"),
            ("created_at", "created_at"),
        ),
        field_labels={
            "price": "Precio",
            "created_at": "Fecha de creación",
        },
    )

    class Meta:
        model = Product
        fields = ["sku", "price_min", "price_max", "q"]
