from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
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
        if Pharmacy.objects.filter(owner=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("This owner already has a pharmacy.")
        serializer.save(owner=self.request.user)


class OwnerDashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        pharmacy = Pharmacy.objects.filter(owner=request.user).first()
        if not pharmacy:
            employee = getattr(request.user, "employee_profile", None)
            pharmacy = employee.pharmacy if employee else None
        if not pharmacy:
            return Response({"pharmacy": None, "stock_count": 0, "units_available": 0, "low_stock": 0})
        stocks = pharmacy.stocks.filter(is_active=True)
        return Response({
            "pharmacy": {"id": pharmacy.id, "name": pharmacy.name},
            "stock_count": stocks.count(),
            "units_available": stocks.aggregate(total=Sum("quantity"))["total"] or 0,
            "low_stock": stocks.filter(quantity__lte=10).count(),
        })
