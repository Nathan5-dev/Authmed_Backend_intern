from rest_framework import viewsets, permissions
from .models import Organization, Site
from .serializers import OrganizationSerializer, SiteSerializer
from authmed_intern.permissions import IsOrgMember
from authmed_intern.mixins import TenantFilterMixin


class OrganizationViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]


class SiteViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
