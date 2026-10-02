from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel
from apps.catalog.models import Medicine
from apps.pharmacies.models import Pharmacy


class PharmacyStock(BaseModel):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="stocks")
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name="inventory_stocks")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("pharmacy", "medicine", "batch_number"), name="unique_pharmacy_medicine_batch"
            )
        ]
        ordering = ("expiry_date",)

    @property
    def selling_price(self):
        return self.price * (Decimal("1") - self.discount_percent / Decimal("100"))

    def __str__(self):
        return f"{self.pharmacy} - {self.medicine} - {self.batch_number}"
