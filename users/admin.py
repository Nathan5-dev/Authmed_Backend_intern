from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "organization", "site", "is_staff")
    list_filter = ("role", "organization", "is_staff")
    search_fields = ("username", "email")
    
    # Define custom fieldsets to include 'role', 'organization', and 'site'
    fieldsets = BaseUserAdmin.fieldsets + (
        ("AuthMed Profile", {"fields": ("role", "organization", "site")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("AuthMed Profile", {"fields": ("role", "organization", "site")}),
    )
