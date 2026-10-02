import uuid
from django.conf import settings
from django.db import models
from apps.core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    icon = models.ImageField(upload_to="catalog/categories/", blank=True, null=True)

    def __str__(self):
        return self.name


class Manufacturer(BaseModel):
    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_medicines",
    )
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="medicines")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name="medicines")
    dosage_form = models.CharField(max_length=80)
    strength = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    uses = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    requires_prescription = models.BooleanField(default=False)
    slug = models.SlugField(max_length=240, unique=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=("name",)),
            models.Index(fields=("generic_name",)),
        ]

    def __str__(self):
        return self.name


class MedicineImage(BaseModel):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="medicines/images/")
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            MedicineImage.objects.filter(medicine=self.medicine, is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )
        super().save(*args, **kwargs)
