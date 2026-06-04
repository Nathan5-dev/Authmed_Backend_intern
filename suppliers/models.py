from django.db import models
from organizations.models import Organization


class Supplier(models.Model):
    """Supplier of medicine batches and products."""

    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name="suppliers",
        null=True,
        blank=True,
        help_text="Organization that works with this supplier"
    )
    name = models.CharField(max_length=255, blank=False)  # Supplier company name (required)
    contact = models.CharField(max_length=255, blank=True)  # Contact person or email (optional)
    address = models.TextField(blank=True)  # Physical address (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # When supplier was added

    def __str__(self):
        return self.name
