from rest_framework import serializers
from .models import BatchInspection, Evidence, RiskResult, ReviewDecision


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ["id", "inspection", "image", "notes", "created_at"]


class RiskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskResult
        fields = ["id", "inspection", "risk_score", "reason", "created_at"]


class ReviewDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewDecision
        fields = ["id", "inspection", "reviewer", "decision", "notes", "created_at"]


from django.utils import timezone

class InspectionSerializer(serializers.ModelSerializer):
    evidences = EvidenceSerializer(many=True, read_only=True)
    risk_result = RiskResultSerializer(read_only=True)
    decisions = ReviewDecisionSerializer(many=True, read_only=True)

    class Meta:
        model = BatchInspection
        fields = [
            "id",
            "organization",
            "site",
            "supplier",
            "product",
            "inspector",
            "batch_number",
            "received_at",
            "created_at",
            "evidences",
            "risk_result",
            "decisions",
        ]

    def validate_batch_number(self, value):
        if not value:
            raise serializers.ValidationError("Batch number is required.")
        return value

    def validate_received_at(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Received date cannot be in the future.")
        return value
