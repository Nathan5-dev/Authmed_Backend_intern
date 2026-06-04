from rest_framework import permissions

class TenantFilterMixin:
    """
    Mixin to automatically filter querysets based on the user's organization.
    Ensures data isolation in a multi-tenant environment.
    """
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Superusers see everything
        if user.is_superuser:
            return queryset
            
        # If the user has no organization (shouldn't happen for non-superusers in this flow),
        # return empty to be safe.
        if not user.organization:
            return queryset.none() if not user.role == "admin" else queryset

        # Special case for Organization model itself
        if self.model.__name__ == 'Organization':
            return queryset.filter(id=user.organization.id)
            
        # Filter by organization if the model has an organization field
        if hasattr(self.model, 'organization'):
            return queryset.filter(organization=user.organization)
            
        return queryset
