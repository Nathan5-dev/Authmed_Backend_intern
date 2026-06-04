from django.contrib import admin
from .models import Organization, Site


class SiteInline(admin.TabularInline):
    model = Site
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    inlines = [SiteInline]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_at")
    list_filter = ("organization",)
    search_fields = ("name",)
