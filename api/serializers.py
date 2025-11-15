"""
Serializers for the API app.
"""

from rest_framework import serializers

from .models import Person, Product


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model."""

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "email", "created_at"]
        read_only_fields = ["id", "created_at"]


class PersonListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Person list view."""

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "email", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    owner = PersonSerializer(read_only=True)
    owner_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "price", "owner", "owner_id", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_sku(self, value):
        """Validate SKU uniqueness on update."""
        if self.instance and self.instance.sku == value:
            return value
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        return value

    def validate_price(self, value):
        """Validate price is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Price must be greater than or equal to 0.")
        return value

    def create(self, validated_data):
        """Create product with optional owner."""
        owner_id = validated_data.pop("owner_id", None)
        if owner_id:
            try:
                owner = Person.objects.get(id=owner_id)
                validated_data["owner"] = owner
            except Person.DoesNotExist:
                raise serializers.ValidationError(
                    {"owner_id": "Person with this ID does not exist."}
                )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update product with optional owner."""
        # Check if owner_id is in validated_data to distinguish between
        # "not provided" and "explicitly set to None"
        if "owner_id" in validated_data:
            owner_id = validated_data.pop("owner_id")
            if owner_id:
                try:
                    owner = Person.objects.get(id=owner_id)
                    validated_data["owner"] = owner
                except Person.DoesNotExist:
                    raise serializers.ValidationError(
                        {"owner_id": "Person with this ID does not exist."}
                    )
            else:
                # owner_id is explicitly None, remove owner
                validated_data["owner"] = None
        return super().update(instance, validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Product list view."""

    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "price", "owner_name", "created_at"]

    def get_owner_name(self, obj):
        """Return owner name or None if no owner."""
        return str(obj.owner) if obj.owner else None
