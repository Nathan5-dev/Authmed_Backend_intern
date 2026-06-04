from django.db import models
from organizations.models import Organization


class AuditLog(models.Model):
    """Audit trail for tracking create/update/delete operations on objects."""
    
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="audit_logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # When the action occurred
    actor = models.CharField(max_length=255, blank=True)  # User who performed the action
    action = models.CharField(max_length=255)  # Type of action (create, update, delete)
    object_type = models.CharField(max_length=128, blank=True)  # Model name of affected object
    object_id = models.CharField(max_length=128, blank=True)  # ID of affected object
    details = models.JSONField(null=True, blank=True)  # Additional context (old/new values, etc.)

    def __str__(self):
        return f"{self.timestamp.isoformat()} {self.actor} {self.action}"
