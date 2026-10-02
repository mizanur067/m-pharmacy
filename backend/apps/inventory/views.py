from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsPharmacyOwner
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
        return queryset.filter(pharmacy__owner=self.request.user)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.IsAuthenticated()]
        return [IsPharmacyOwner()]

    def perform_create(self, serializer):
        pharmacy_id = self.request.data.get("pharmacy")
        pharmacy = Pharmacy.objects.filter(id=pharmacy_id, owner=self.request.user).first()
        if not pharmacy:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only manage stock for your own pharmacy.")
        serializer.save(pharmacy=pharmacy)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
