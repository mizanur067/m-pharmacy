from rest_framework import serializers
from .models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = (
            "id", "name", "license_number", "address", "phone", "hours",
            "logo", "verification_status", "owner", "created_at", "updated_at",
        )
        read_only_fields = ("id", "owner", "verification_status", "created_at", "updated_at")
