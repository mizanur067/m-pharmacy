from rest_framework.permissions import BasePermission


class IsPharmacyStockOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.pharmacy.owner_id == request.user.id
