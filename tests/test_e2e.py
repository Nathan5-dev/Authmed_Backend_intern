from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from organizations.models import Organization, Site
from users.models import User
from products.models import ProductReference
from suppliers.models import Supplier
from inspections.models import BatchInspection

class TestEndToEndWorkflow(APITestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="E2E Corp")
        self.site = Site.objects.create(name="E2E Warehouse", organization=self.org)
        self.inspector = User.objects.create_user(
            username="inspector_e2e", 
            password="password123", 
            organization=self.org,
            role="inspector"
        )
        self.reviewer = User.objects.create_user(
            username="reviewer_e2e", 
            password="password123", 
            organization=self.org,
            role="admin"
        )
        self.product = ProductReference.objects.create(
            organization=self.org, name="Med-X 500mg", sku="MEDX-123"
        )
        self.supplier = Supplier.objects.create(
            organization=self.org, name="GlobalPharma"
        )

    def test_full_inspection_flow(self):
        # 1. Authenticate
        login_url = reverse('token_obtain_pair')
        response = self.client.post(login_url, {"username": "inspector_e2e", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # 2. Create BatchInspection
        # Note: Depending on router, might be 'batchinspection-list' or 'batch-inspections-list'
        # Let's try to be safe and check if it fails
        insp_url = reverse('batchinspection-list')
        insp_data = {
            "organization": self.org.id,
            "site": self.site.id,
            "batch_number": "BATCH-E2E-001",
            "received_at": "2024-01-01T10:00:00Z"
        }
        response = self.client.post(insp_url, insp_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        insp_id = response.data['id']

        # 3. Add Evidence with OCR text (notes)
        evidence_url = reverse('batchinspection-add-evidence', args=[insp_id])
        evidence_data = {
            "notes": "MEDX-123", 
            "image": None
        }
        response = self.client.post(evidence_url, evidence_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify matching
        inspection = BatchInspection.objects.get(id=insp_id)
        self.assertEqual(inspection.product, self.product)

        # 4. Generate RiskResult (High Risk)
        risk_url = reverse('riskresult-list')
        risk_data = {
            "inspection": insp_id,
            "risk_score": 85,
            "reason": "Suspicious packaging detected via OCR analysis."
        }
        response = self.client.post(risk_url, risk_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify automatic isolation
        inspection.refresh_from_db()
        self.assertEqual(inspection.outcome, "isolated")

        # 5. Reviewer Decision
        response = self.client.post(login_url, {"username": "reviewer_e2e", "password": "password123"})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

        decision_url = reverse('reviewdecision-list')
        decision_data = {
            "inspection": insp_id,
            "decision": "rejected",
            "notes": "Confirmed non-compliance."
        }
        response = self.client.post(decision_url, decision_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
