"""
Tests for API serializers validation.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Person, Product


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.mark.django_db
class TestProductSerializerValidation:
    """Tests for Product serializer validations."""

    def test_create_product_with_duplicate_sku(self, api_client):
        """Test creating a product with duplicate SKU fails."""
        Product.objects.create(name="Product 1", sku="DUPLICATE-001", price="99.99")

        url = reverse("product-list")
        data = {"name": "Product 2", "sku": "DUPLICATE-001", "price": "149.99"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "sku" in response.data

    def test_create_product_with_negative_price(self, api_client):
        """Test creating a product with negative price fails."""
        url = reverse("product-list")
        data = {"name": "Product", "sku": "NEG-001", "price": "-10.00"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in response.data

    def test_update_product_with_duplicate_sku(self, api_client):
        """Test updating a product with duplicate SKU fails."""
        product1 = Product.objects.create(name="Product 1", sku="SKU-001", price="99.99")
        product2 = Product.objects.create(name="Product 2", sku="SKU-002", price="149.99")

        url = reverse("product-detail", kwargs={"pk": product1.id})
        data = {"name": "Product 1", "sku": "SKU-002", "price": "99.99"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "sku" in response.data

    def test_update_product_with_same_sku_succeeds(self, api_client):
        """Test updating a product with same SKU succeeds."""
        product = Product.objects.create(name="Product 1", sku="SKU-001", price="99.99")

        url = reverse("product-detail", kwargs={"pk": product.id})
        data = {"name": "Updated Product", "sku": "SKU-001", "price": "149.99"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_create_product_with_invalid_owner_id(self, api_client):
        """Test creating a product with invalid owner_id fails."""
        import uuid

        url = reverse("product-list")
        data = {
            "name": "Product",
            "sku": "INV-001",
            "price": "99.99",
            "owner_id": str(uuid.uuid4()),  # Non-existent UUID
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "owner_id" in response.data

    def test_update_product_with_invalid_owner_id(self, api_client):
        """Test updating a product with invalid owner_id fails."""
        import uuid

        product = Product.objects.create(name="Product", sku="UPD-001", price="99.99")

        url = reverse("product-detail", kwargs={"pk": product.id})
        data = {
            "name": "Product",
            "sku": "UPD-001",
            "price": "99.99",
            "owner_id": str(uuid.uuid4()),  # Non-existent UUID
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "owner_id" in response.data

    def test_update_product_remove_owner(self, api_client):
        """Test updating a product to remove owner."""
        person = Person.objects.create(
            first_name="John", last_name="Doe", email="john@example.com"
        )
        product = Product.objects.create(
            name="Product", sku="OWN-001", price="99.99", owner=person
        )

        url = reverse("product-detail", kwargs={"pk": product.id})
        # Use empty string or explicitly set to null - DRF handles null in JSON
        data = {"name": "Product", "sku": "OWN-001", "price": "99.99"}
        # First verify owner exists
        assert product.owner is not None
        
        # Use PATCH to only update owner_id to null
        patch_data = {"owner_id": None}
        response = api_client.patch(url, patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        
        product.refresh_from_db()
        assert product.owner is None
        # Verify response shows owner as None
        assert response.data.get("owner") is None

