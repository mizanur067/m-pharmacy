from datetime import date, timedelta
from decimal import Decimal
import pytest
from apps.accounts.models import User
from apps.catalog.models import Category, Manufacturer, Medicine
from apps.inventory.models import PharmacyStock
from apps.orders.services import add_to_cart, place_order
from apps.pharmacies.models import Pharmacy
from rest_framework.exceptions import ValidationError


@pytest.fixture
def order_setup():
    customer = User.objects.create_user("customer@example.com", "Strong-password-123")
    owner = User.objects.create_user("owner2@example.com", "Strong-password-123", role=User.Role.PHARMACY_OWNER)
    pharmacy = Pharmacy.objects.create(owner=owner, name="Order Pharmacy", license_number="LIC-ORDER", address="Main", phone="1")
    medicine = Medicine.objects.create(
        name="Order medicine", generic_name="Generic", category=Category.objects.create(name="Cat", slug="cat"),
        manufacturer=Manufacturer.objects.create(name="Maker", slug="maker"), dosage_form="tablet",
        strength="10mg", slug="order-medicine",
    )
    stock = PharmacyStock.objects.create(
        pharmacy=pharmacy, medicine=medicine, price=Decimal("12.00"), quantity=2,
        batch_number="ORDER-1", expiry_date=date.today() + timedelta(days=30),
    )
    return customer, stock


@pytest.mark.django_db
def test_place_order_decrements_stock(order_setup):
    customer, stock = order_setup
    add_to_cart(customer, stock, 1)
    order = place_order(customer, "10 Main Street")
    stock.refresh_from_db()
    assert order.total == Decimal("12.00")
    assert stock.quantity == 1


@pytest.mark.django_db
def test_expired_stock_cannot_be_added(order_setup):
    customer, stock = order_setup
    stock.expiry_date = date.today() - timedelta(days=1)
    stock.save(update_fields=["expiry_date"])
    with pytest.raises(ValidationError):
        add_to_cart(customer, stock, 1)
