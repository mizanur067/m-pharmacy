from rest_framework import serializers
from .models import PharmacyStock


class PharmacyStockSerializer(serializers.ModelSerializer):
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)

    class Meta:
        model = PharmacyStock
        fields = (
            "id", "pharmacy", "pharmacy_name", "medicine", "medicine_name", "price",
            "discount_percent", "selling_price", "quantity", "batch_number",
            "expiry_date", "is_available",
        )
        read_only_fields = ("id", "pharmacy")

    def validate(self, attrs):
        if attrs.get("price", 0) < 0:
            raise serializers.ValidationError({"price": "Price cannot be negative."})
        if attrs.get("discount_percent", 0) > 100:
            raise serializers.ValidationError({"discount_percent": "Discount cannot exceed 100%."})
        return attrs
