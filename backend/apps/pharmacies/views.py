from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsPharmacyOwner
from .models import Pharmacy
from .serializers import PharmacySerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Pharmacy.objects.select_related("owner").filter(is_active=True)
        if self.request.user.is_staff:
            return queryset
        if self.action in ("list", "retrieve"):
            return queryset.filter(verification_status=Pharmacy.VerificationStatus.APPROVED)
        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsPharmacyOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
