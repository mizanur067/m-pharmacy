from rest_framework import serializers
from .models import Category, Manufacturer, Medicine, MedicineImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon")


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "slug")


class MedicineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineImage
        fields = ("id", "image", "is_primary", "alt_text")
        read_only_fields = ("id",)


class MedicineSerializer(serializers.ModelSerializer):
    images = MedicineImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    manufacturer_name = serializers.CharField(source="manufacturer.name", read_only=True)

    class Meta:
        model = Medicine
        fields = (
            "id", "name", "generic_name", "category", "category_name",
            "manufacturer", "manufacturer_name", "dosage_form", "strength",
            "description", "uses", "side_effects", "requires_prescription",
            "slug", "images",
        )
        read_only_fields = ("id", "images", "created_by")
