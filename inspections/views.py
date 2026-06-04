from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BatchInspection, Evidence, RiskResult, ReviewDecision
from .serializers import (
    InspectionSerializer,
    EvidenceSerializer,
    RiskResultSerializer,
    ReviewDecisionSerializer,
)
from authmed_intern.permissions import IsOrgMember
from authmed_intern.mixins import TenantFilterMixin


import logging

logger = logging.getLogger(__name__)


class InspectionViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = BatchInspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    @action(detail=True, methods=["post"])
    def add_evidence(self, request, pk=None):
        """
        Add evidence to an inspection and trigger automatic matching logic if OCR text is provided.
        """
        insp = self.get_object()
        serializer = EvidenceSerializer(data=request.data)
        if serializer.is_valid():
            evidence = serializer.save(inspection=insp)
            
            # Extract OCR text from notes or a dedicated field if added
            ocr_text = request.data.get("notes", "")
            if ocr_text:
                logger.info(f"Triggering matching for Inspection {insp.id} with text: {ocr_text}")
                insp.match_references(ocr_text)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        logger.warning(f"Failed evidence submission for Inspection {insp.id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvidenceViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]


class RiskResultViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = RiskResult.objects.all()
    serializer_class = RiskResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def perform_create(self, serializer):
        risk_result = serializer.save()
        # Automatically isolation if risk is too high
        if risk_result.risk_score > 75:
            logger.info(f"High risk score {risk_result.risk_score} for inspection {risk_result.inspection.id}. Isolation recommended.")
            risk_result.inspection.outcome = "isolated"
            risk_result.inspection.save()


class ReviewDecisionViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = ReviewDecision.objects.all()
    serializer_class = ReviewDecisionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgMember]
