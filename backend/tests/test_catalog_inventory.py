from datetime import date, timedelta
from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.catalog.models import Category, Manufacturer, Medicine
from apps.inventory.models import PharmacyStock
from apps.pharmacies.models import Pharmacy


@pytest.fixture
def owner():
    return User.objects.create_user("owner@example.com", "Strong-password-123", role=User.Role.PHARMACY_OWNER)


@pytest.fixture
def pharmacy(owner):
    return Pharmacy.objects.create(
        owner=owner, name="Care Pharmacy", license_number="LIC-1", address="1 Main St", phone="123"
    )


@pytest.fixture
def medicine():
    category = Category.objects.create(name="Pain relief", slug="pain-relief")
    manufacturer = Manufacturer.objects.create(name="Acme", slug="acme")
    return Medicine.objects.create(
        name="Example", generic_name="Example generic", category=category, manufacturer=manufacturer,
        dosage_form="tablet", strength="500mg", slug="example",
    )


@pytest.mark.django_db
def test_owner_can_create_pharmacy_and_stock(owner, pharmacy, medicine):
    client = APIClient()
    client.force_authenticate(owner)
    response = client.post("/api/v1/inventory/stocks/", {
        "pharmacy": str(pharmacy.id), "medicine": str(medicine.id), "price": "10.00",
        "quantity": 4, "batch_number": "B1", "expiry_date": str(date.today() + timedelta(days=30)),
    })
    assert response.status_code == 201
    assert PharmacyStock.objects.get().selling_price == Decimal("10.00")


@pytest.mark.django_db
def test_non_owner_cannot_manage_pharmacy(owner, pharmacy):
    other = User.objects.create_user("other@example.com", "Strong-password-123", role=User.Role.PHARMACY_OWNER)
    client = APIClient()
    client.force_authenticate(other)
    response = client.patch(f"/api/v1/pharmacies/{pharmacy.id}/", {"name": "Changed"})
    assert response.status_code == 404


@pytest.mark.django_db
def test_presign_rejects_unsupported_type(owner):
    client = APIClient()
    client.force_authenticate(owner)
    response = client.post("/api/v1/uploads/presign/", {"kind": "image", "content_type": "text/plain", "size": 20})
    assert response.status_code == 400
