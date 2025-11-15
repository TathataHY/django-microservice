"""
Models for the API app.
"""

import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models


def validate_email(value):
    """Validate email format."""
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError("Invalid email format.")


class Person(models.Model):
    """
    Person model with UUID primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        help_text="First name (1-100 characters)",
    )
    last_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        help_text="Last name (1-100 characters)",
    )
    email = models.EmailField(
        unique=True, validators=[validate_email], help_text="Unique email address"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "persons"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Product(models.Model):
    """
    Product model with UUID primary key and optional owner relationship.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(1), MaxLengthValidator(150)],
        help_text="Product name (1-150 characters)",
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        help_text="Unique SKU (3-50 characters)",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price (≥ 0, 2 decimal places)",
    )
    owner = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="Optional owner (Person)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} (SKU: {self.sku}) - ${self.price}"
