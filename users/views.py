from authmed_intern.permissions import IsAdmin
from authmed_intern.mixins import TenantFilterMixin


class UserViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAdmin()]
        return super().get_permissions()
