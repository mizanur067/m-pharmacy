from django.conf import settings
from django.db import models
from apps.core.models import BaseModel


class Pharmacy(BaseModel):
    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pharmacies")
    name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    hours = models.JSONField(default=dict, blank=True)
    logo = models.ImageField(upload_to="pharmacies/logos/", blank=True, null=True)
    verification_status = models.CharField(
        max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
