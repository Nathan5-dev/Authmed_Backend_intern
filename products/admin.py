from django.contrib import admin
from .models import ProductReference


@admin.register(ProductReference)
class ProductReferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "organization", "created_at")
    list_filter = ("organization",)
    search_fields = ("name", "sku")
