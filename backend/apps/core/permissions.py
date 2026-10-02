from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    role = ""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == self.role)


class IsCustomer(IsRole):
    role = "customer"


class IsPharmacyOwner(IsRole):
    role = "pharmacy_owner"


class IsDoctor(IsRole):
    role = "doctor"

