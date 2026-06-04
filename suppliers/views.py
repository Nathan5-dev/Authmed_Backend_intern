from rest_framework import viewsets, permissions
from .models import Supplier
from .serializers import SupplierSerializer
from authmed_intern.permissions import IsOrgMember
from authmed_intern.mixins import TenantFilterMixin


class SupplierViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
