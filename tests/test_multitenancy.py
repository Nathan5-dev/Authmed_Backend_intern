import pytest
from django.urls import reverse
from rest_framework import status
from organizations.models import Organization
from users.models import User
from suppliers.models import Supplier

@pytest.mark.django_db
class TestMultiTenancy:
    def setup_method(self):
        self.org_a = Organization.objects.create(name="Org A")
        self.org_b = Organization.objects.create(name="Org B")
        
        self.user_a = User.objects.create_user(
            username="user_a", 
            password="password", 
            organization=self.org_a,
            role="inspector"
        )
        self.user_b = User.objects.create_user(
            username="user_b", 
            password="password", 
            organization=self.org_b,
            role="inspector"
        )
        
        self.supplier_a = Supplier.objects.create(name="Supplier A", organization=self.org_a)
        self.supplier_b = Supplier.objects.create(name="Supplier B", organization=self.org_b)

    def test_user_a_cannot_see_supplier_b(self, client):
        client.force_authenticate(user=self.user_a)
        url = reverse('supplier-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Should only see Supplier A
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Supplier A"

    def test_user_a_cannot_access_supplier_b_detail(self, client):
        client.force_authenticate(user=self.user_a)
        url = reverse('supplier-detail', args=[self.supplier_b.id])
        response = client.get(url)
        # Detail view should return 404 because queryset is filtered
        assert response.status_code == status.HTTP_404_NOT_FOUND
