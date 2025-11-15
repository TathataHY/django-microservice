"""
Tests for API models.
"""

import uuid

import pytest
from django.core.exceptions import ValidationError

from api.models import Person, Product


@pytest.mark.django_db
class TestPersonModel:
    """Tests for Person model."""

    def test_create_person(self):
        """Test creating a person."""
        person = Person.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        assert person.id is not None
        assert isinstance(person.id, uuid.UUID)
        assert person.first_name == "John"
        assert person.last_name == "Doe"
        assert person.email == "john.doe@example.com"
        assert person.created_at is not None

    def test_person_str(self):
        """Test Person string representation."""
        person = Person.objects.create(
            first_name="Jane", last_name="Smith", email="jane.smith@example.com"
        )
        assert "Jane" in str(person)
        assert "Smith" in str(person)
        assert "jane.smith@example.com" in str(person)

    def test_person_email_unique(self):
        """Test that email must be unique."""
        Person.objects.create(first_name="John", last_name="Doe", email="test@example.com")
        with pytest.raises(Exception):  # IntegrityError
            Person.objects.create(first_name="Jane", last_name="Doe", email="test@example.com")

    def test_person_email_validation(self):
        """Test that email format is validated."""
        person = Person(first_name="John", last_name="Doe", email="invalid-email")
        with pytest.raises(ValidationError):
            person.full_clean()


@pytest.mark.django_db
class TestProductModel:
    """Tests for Product model."""

    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(name="Test Product", sku="TEST-001", price="99.99")
        assert product.id is not None
        assert isinstance(product.id, uuid.UUID)
        assert product.name == "Test Product"
        assert product.sku == "TEST-001"
        assert float(product.price) == 99.99
        assert product.owner is None
        assert product.created_at is not None

    def test_create_product_with_owner(self):
        """Test creating a product with owner."""
        person = Person.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        product = Product.objects.create(
            name="Test Product", sku="TEST-002", price="149.99", owner=person
        )
        assert product.owner == person
        assert product in person.products.all()

    def test_product_str(self):
        """Test Product string representation."""
        product = Product.objects.create(name="Amazing Product", sku="AMZ-001", price="199.99")
        assert "Amazing Product" in str(product)
        assert "AMZ-001" in str(product)
        assert "199.99" in str(product)

    def test_product_sku_unique(self):
        """Test that SKU must be unique."""
        Product.objects.create(name="Product 1", sku="UNIQUE-001", price="99.99")
        with pytest.raises(Exception):  # IntegrityError
            Product.objects.create(name="Product 2", sku="UNIQUE-001", price="149.99")

    def test_product_price_non_negative(self):
        """Test that price cannot be negative."""
        product = Product(name="Test Product", sku="TEST-003", price="-10.00")
        with pytest.raises(ValidationError):
            product.full_clean()
