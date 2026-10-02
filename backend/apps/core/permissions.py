from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    role = ""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == self.role)


class IsCustomer(IsRole):
    role = "customer"


class IsPharmacyOwner(IsRole):
    role = "pharmacy_owner"


class IsPharmacyEmployee(IsRole):
    role = "employee"


class IsOwnerOrEmployee(BasePermission):
    allowed_roles = {"pharmacy_owner", "employee"}

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role in self.allowed_roles)


class IsDoctor(IsRole):
    role = "doctor"
