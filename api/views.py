"""
Views for the API app.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import PersonFilter, ProductFilter
from .models import Person, Product
from .serializers import (
    PersonListSerializer,
    PersonSerializer,
    ProductListSerializer,
    ProductSerializer,
)


class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Person CRUD operations.

    list: List all persons with pagination and filters (email, last_name, ordering by created_at)
    retrieve: Get a specific person by ID
    create: Create a new person
    update: Update a person (PUT)
    partial_update: Partially update a person (PATCH)
    destroy: Delete a person
    """

    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PersonFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == "list":
            return PersonListSerializer
        return PersonSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations.

    list: List all products with pagination and filters (sku, price_min, price_max, q for name search, ordering by price/created_at)
    retrieve: Get a specific product by ID
    create: Create a new product
    update: Update a product (PUT)
    partial_update: Partially update a product (PATCH)
    destroy: Delete a product
    """

    queryset = Product.objects.select_related("owner").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer
