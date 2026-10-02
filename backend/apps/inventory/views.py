from rest_framework import permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsOwnerOrEmployee
from apps.pharmacies.models import Pharmacy
from .models import PharmacyStock
from .permissions import IsPharmacyStockOwner
from .serializers import PharmacyStockSerializer


class PharmacyStockViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacyStockSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("pharmacy", "medicine", "is_available")

    def get_queryset(self):
        queryset = PharmacyStock.objects.select_related("pharmacy", "medicine").filter(is_active=True)
        if self.request.user.is_staff:
            return queryset
        if self.action in ("list", "retrieve"):
            return queryset.filter(
                pharmacy__verification_status=Pharmacy.VerificationStatus.APPROVED,
                pharmacy__is_active=True,
                quantity__gt=0,
                is_available=True,
            ).distinct()
        return queryset.filter(
            models.Q(pharmacy__owner=self.request.user) | models.Q(pharmacy__employees__user=self.request.user)
        ).distinct()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [IsOwnerOrEmployee()]

    def perform_create(self, serializer):
        pharmacy_id = self.request.data.get("pharmacy")
        pharmacy = Pharmacy.objects.filter(id=pharmacy_id).filter(
            models.Q(owner=self.request.user) | models.Q(employees__user=self.request.user)
        ).first()
        if not pharmacy:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only manage stock for your own pharmacy.")
        serializer.save(pharmacy=pharmacy)

    def get_object(self):
        obj = super().get_object()
        if not (
            obj.pharmacy.owner_id == self.request.user.id
            or obj.pharmacy.employees.filter(user=self.request.user).exists()
            or self.request.user.is_staff
        ):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot manage this pharmacy stock.")
        self.check_object_permissions(self.request, obj)
        return obj
