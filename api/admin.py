"""
Admin configuration for API models.
"""

from django.contrib import admin

from .models import Person, Product


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["first_name", "last_name", "email"]
    readonly_fields = ["id", "created_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sku", "price", "owner", "created_at"]
    list_filter = ["created_at", "owner"]
    search_fields = ["name", "sku"]
    readonly_fields = ["id", "created_at"]
    autocomplete_fields = ["owner"]
