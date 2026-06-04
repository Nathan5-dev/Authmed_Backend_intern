from django.contrib import admin
from django.utils.html import format_html
from .models import BatchInspection, Evidence, RiskResult, ReviewDecision


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 150px;"/>', obj.image.url)
        return "No image"


class RiskResultInline(admin.StackedInline):
    model = RiskResult
    extra = 0


class ReviewDecisionInline(admin.StackedInline):
    model = ReviewDecision
    extra = 0


@admin.register(BatchInspection)
class BatchInspectionAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "product", "supplier", "inspector", "outcome", "received_at")
    list_filter = ("outcome", "organization", "site")
    search_fields = ("batch_number", "product__name", "supplier__name")
    inlines = [EvidenceInline, RiskResultInline, ReviewDecisionInline]
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Header Info", {"fields": ("organization", "site", "inspector")}),
        ("Product Details", {"fields": ("product", "supplier", "batch_number", "received_at")}),
        ("Final Outcome", {"fields": ("outcome",)}),
    )


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("id", "inspection", "image_tag", "created_at")
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "No image"


@admin.register(RiskResult)
class RiskResultAdmin(admin.ModelAdmin):
    list_display = ("inspection", "risk_score", "created_at")
    list_filter = ("risk_score",)


@admin.register(ReviewDecision)
class ReviewDecisionAdmin(admin.ModelAdmin):
    list_display = ("inspection", "reviewer", "decision", "created_at")
    list_filter = ("decision",)
