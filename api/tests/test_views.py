"""
Tests for API views.
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


@pytest.fixture
def person_data():
    """Sample person data."""
    return {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}


@pytest.fixture
def product_data():
    """Sample product data."""
    return {"name": "Test Product", "sku": "TEST-001", "price": "99.99"}


@pytest.mark.django_db
class TestPersonViewSet:
    """Tests for Person ViewSet."""

    def test_create_person(self, api_client, person_data):
        """Test creating a person via API."""
        url = reverse("person-list")
        response = api_client.post(url, person_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["first_name"] == person_data["first_name"]
        assert response.data["last_name"] == person_data["last_name"]
        assert response.data["email"] == person_data["email"]
        assert "id" in response.data
        assert "created_at" in response.data

    def test_list_persons(self, api_client, person_data):
        """Test listing persons."""
        # Create test data
        Person.objects.create(**person_data)
        Person.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")

        url = reverse("person-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2

    def test_list_persons_pagination(self, api_client):
        """Test pagination in person list."""
        # Create 25 persons
        for i in range(25):
            Person.objects.create(
                first_name=f"Person{i}", last_name="Test", email=f"person{i}@example.com"
            )

        url = reverse("person-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 25
        assert len(response.data["results"]) == 20  # Default page size
        assert "next" in response.data
        assert "previous" in response.data

    def test_filter_persons_by_email(self, api_client):
        """Test filtering persons by email."""
        Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        Person.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")

        url = reverse("person-list")
        response = api_client.get(url, {"email": "john"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["email"] == "john.doe@example.com"

    def test_filter_persons_by_last_name(self, api_client):
        """Test filtering persons by last name."""
        Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        Person.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")

        url = reverse("person-list")
        response = api_client.get(url, {"last_name": "Smith"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["last_name"] == "Smith"

    def test_retrieve_person(self, api_client, person_data):
        """Test retrieving a specific person."""
        person = Person.objects.create(**person_data)
        url = reverse("person-detail", kwargs={"pk": person.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == person_data["email"]

    def test_update_person(self, api_client, person_data):
        """Test updating a person."""
        person = Person.objects.create(**person_data)
        url = reverse("person-detail", kwargs={"pk": person.id})
        update_data = {"first_name": "Updated", "last_name": "Name", "email": "updated@example.com"}
        response = api_client.put(url, update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"

        person.refresh_from_db()
        assert person.first_name == "Updated"

    def test_partial_update_person(self, api_client, person_data):
        """Test partially updating a person."""
        person = Person.objects.create(**person_data)
        url = reverse("person-detail", kwargs={"pk": person.id})
        response = api_client.patch(url, {"first_name": "Updated"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == person_data["last_name"]  # Unchanged

    def test_delete_person(self, api_client, person_data):
        """Test deleting a person."""
        person = Person.objects.create(**person_data)
        url = reverse("person-detail", kwargs={"pk": person.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Person.objects.filter(id=person.id).exists()

    def test_order_persons_by_created_at_ascending(self, api_client):
        """Test ordering persons by created_at ascending."""
        from django.utils import timezone
        import time

        # Create persons with slight delay to ensure different created_at
        person1 = Person.objects.create(
            first_name="First", last_name="Person", email="first@example.com"
        )
        time.sleep(0.01)  # Small delay to ensure different timestamps
        person2 = Person.objects.create(
            first_name="Second", last_name="Person", email="second@example.com"
        )

        url = reverse("person-list")
        response = api_client.get(url, {"ordering": "created_at"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        # First person should be first (ascending order)
        assert response.data["results"][0]["email"] == "first@example.com"
        assert response.data["results"][1]["email"] == "second@example.com"

    def test_order_persons_by_created_at_descending(self, api_client):
        """Test ordering persons by created_at descending (default)."""
        from django.utils import timezone
        import time

        # Create persons with slight delay
        person1 = Person.objects.create(
            first_name="First", last_name="Person", email="first@example.com"
        )
        time.sleep(0.01)
        person2 = Person.objects.create(
            first_name="Second", last_name="Person", email="second@example.com"
        )

        url = reverse("person-list")
        response = api_client.get(url, {"ordering": "-created_at"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        # Second person should be first (descending order)
        assert response.data["results"][0]["email"] == "second@example.com"
        assert response.data["results"][1]["email"] == "first@example.com"


@pytest.mark.django_db
class TestProductViewSet:
    """Tests for Product ViewSet."""

    def test_create_product(self, api_client, product_data):
        """Test creating a product via API."""
        url = reverse("product-list")
        response = api_client.post(url, product_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == product_data["name"]
        assert response.data["sku"] == product_data["sku"]
        assert response.data["price"] == product_data["price"]
        assert "id" in response.data
        assert "created_at" in response.data

    def test_create_product_with_owner(self, api_client, product_data):
        """Test creating a product with owner."""
        person = Person.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        product_data["owner_id"] = str(person.id)
        url = reverse("product-list")
        response = api_client.post(url, product_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["owner"]["email"] == person.email

    def test_list_products(self, api_client, product_data):
        """Test listing products."""
        Product.objects.create(**product_data)
        Product.objects.create(name="Another Product", sku="TEST-002", price="149.99")

        url = reverse("product-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_filter_products_by_sku(self, api_client):
        """Test filtering products by SKU."""
        Product.objects.create(name="Product 1", sku="SKU-001", price="99.99")
        Product.objects.create(name="Product 2", sku="SKU-002", price="149.99")

        url = reverse("product-list")
        response = api_client.get(url, {"sku": "SKU-001"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["sku"] == "SKU-001"

    def test_filter_products_by_price_range(self, api_client):
        """Test filtering products by price range."""
        Product.objects.create(name="Cheap", sku="CH-001", price="10.00")
        Product.objects.create(name="Medium", sku="MD-001", price="50.00")
        Product.objects.create(name="Expensive", sku="EX-001", price="100.00")

        url = reverse("product-list")
        response = api_client.get(url, {"price_min": "20.00", "price_max": "80.00"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["sku"] == "MD-001"

    def test_search_products_by_name(self, api_client):
        """Test searching products by name."""
        Product.objects.create(name="Laptop Computer", sku="LP-001", price="999.99")
        Product.objects.create(name="Desktop Computer", sku="DT-001", price="799.99")
        Product.objects.create(name="Mouse", sku="MS-001", price="29.99")

        url = reverse("product-list")
        response = api_client.get(url, {"q": "Computer"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_retrieve_product(self, api_client, product_data):
        """Test retrieving a specific product."""
        product = Product.objects.create(**product_data)
        url = reverse("product-detail", kwargs={"pk": product.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["sku"] == product_data["sku"]

    def test_update_product(self, api_client, product_data):
        """Test updating a product."""
        product = Product.objects.create(**product_data)
        url = reverse("product-detail", kwargs={"pk": product.id})
        update_data = {"name": "Updated Product", "sku": "UPD-001", "price": "199.99"}
        response = api_client.put(url, update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Product"

    def test_delete_product(self, api_client, product_data):
        """Test deleting a product."""
        product = Product.objects.create(**product_data)
        url = reverse("product-detail", kwargs={"pk": product.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product.id).exists()

    def test_partial_update_product(self, api_client, product_data):
        """Test partially updating a product."""
        product = Product.objects.create(**product_data)
        url = reverse("product-detail", kwargs={"pk": product.id})
        response = api_client.patch(url, {"name": "Updated Name"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Name"
        assert response.data["sku"] == product_data["sku"]  # Unchanged
        assert response.data["price"] == product_data["price"]  # Unchanged

    def test_order_products_by_price_ascending(self, api_client):
        """Test ordering products by price ascending."""
        Product.objects.create(name="Expensive", sku="EXP-001", price="100.00")
        Product.objects.create(name="Cheap", sku="CHP-001", price="10.00")
        Product.objects.create(name="Medium", sku="MED-001", price="50.00")

        url = reverse("product-list")
        response = api_client.get(url, {"ordering": "price"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        # Should be ordered by price ascending
        assert response.data["results"][0]["sku"] == "CHP-001"
        assert response.data["results"][1]["sku"] == "MED-001"
        assert response.data["results"][2]["sku"] == "EXP-001"

    def test_order_products_by_price_descending(self, api_client):
        """Test ordering products by price descending."""
        Product.objects.create(name="Expensive", sku="EXP-001", price="100.00")
        Product.objects.create(name="Cheap", sku="CHP-001", price="10.00")
        Product.objects.create(name="Medium", sku="MED-001", price="50.00")

        url = reverse("product-list")
        response = api_client.get(url, {"ordering": "-price"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        # Should be ordered by price descending
        assert response.data["results"][0]["sku"] == "EXP-001"
        assert response.data["results"][1]["sku"] == "MED-001"
        assert response.data["results"][2]["sku"] == "CHP-001"

    def test_order_products_by_created_at(self, api_client):
        """Test ordering products by created_at."""
        import time

        product1 = Product.objects.create(name="First", sku="FIR-001", price="10.00")
        time.sleep(0.01)
        product2 = Product.objects.create(name="Second", sku="SEC-001", price="20.00")

        url = reverse("product-list")
        response = api_client.get(url, {"ordering": "-created_at"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        # Second product should be first (descending order)
        assert response.data["results"][0]["sku"] == "SEC-001"
        assert response.data["results"][1]["sku"] == "FIR-001"
