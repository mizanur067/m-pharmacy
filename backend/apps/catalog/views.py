from rest_framework import permissions, viewsets
from apps.core.permissions import IsOwnerOrEmployee
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MedicineFilter
from .models import Category, Manufacturer, Medicine
from .serializers import CategorySerializer, ManufacturerSerializer, MedicineSerializer


class PublicReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)


class CategoryViewSet(PublicReadOnlyViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ManufacturerViewSet(PublicReadOnlyViewSet):
    queryset = Manufacturer.objects.filter(is_active=True)
    serializer_class = ManufacturerSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MedicineFilter
    ordering_fields = ("name", "created_at")
    search_fields = ("name", "generic_name", "manufacturer__name")

    def get_queryset(self):
        return Medicine.objects.filter(is_active=True).select_related("category", "manufacturer").prefetch_related("images")

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsOwnerOrEmployee()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
