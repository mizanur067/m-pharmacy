from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "license_number", "verification_status", "is_active")
    list_filter = ("verification_status", "is_active")
    search_fields = ("name", "license_number", "owner__email")
