from django.contrib import admin
from .models import PharmacyStock


@admin.register(PharmacyStock)
class PharmacyStockAdmin(admin.ModelAdmin):
    list_display = ("pharmacy", "medicine", "batch_number", "quantity", "expiry_date", "is_available")
    list_filter = ("is_available", "expiry_date")
    search_fields = ("pharmacy__name", "medicine__name", "batch_number")
