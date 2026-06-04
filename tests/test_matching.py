import pytest
from django.utils import timezone
from organizations.models import Organization, Site
from users.models import User
from products.models import ProductReference
from suppliers.models import Supplier
from inspections.models import BatchInspection

@pytest.mark.django_db
class TestMatchingLogic:
    def setup_method(self):
        self.org = Organization.objects.create(name="Match Test Org")
        self.site = Site.objects.create(name="Match Lab", organization=self.org)
        self.user = User.objects.create_user(
            username="match_inspector", password="password", organization=self.org, role="inspector"
        )
        self.product = ProductReference.objects.create(
            organization=self.org, name="Aspirin", sku="ASP123"
        )
        self.supplier = Supplier.objects.create(
            organization=self.org, name="PharmaCorp"
        )
        self.inspection = BatchInspection.objects.create(
            organization=self.org, 
            site=self.site,
            batch_number="B002",
            received_at=timezone.now()
        )

    def test_matching_product_by_sku(self):
        self.inspection.match_references("ASP123")
        self.inspection.refresh_from_db()
        assert self.inspection.product == self.product

    def test_matching_supplier_by_name(self):
        self.inspection.match_references("PharmaCorp")
        self.inspection.refresh_from_db()
        assert self.inspection.supplier == self.supplier
