from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_at")
    list_filter = ("organization",)
    search_fields = ("name",)
