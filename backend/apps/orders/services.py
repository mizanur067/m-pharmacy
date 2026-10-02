from datetime import date
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Cart, CartItem, Order, OrderItem


@transaction.atomic
def add_to_cart(customer, stock, quantity):
    if stock.expiry_date <= date.today():
        raise ValidationError("Expired stock cannot be purchased.")
    if not stock.is_available or stock.quantity < quantity:
        raise ValidationError("Requested quantity is not available.")
    cart, _ = Cart.objects.get_or_create(customer=customer)
    if cart.pharmacy_id and cart.pharmacy_id != stock.pharmacy_id:
        raise ValidationError("A cart can contain medicines from one pharmacy only.")
    cart.pharmacy = stock.pharmacy
    cart.save(update_fields=["pharmacy", "updated_at"])
    item, created = CartItem.objects.get_or_create(cart=cart, stock=stock, defaults={"quantity": quantity})
    if not created:
        if item.quantity + quantity > stock.quantity:
            raise ValidationError("Requested quantity is not available.")
        item.quantity += quantity
        item.save(update_fields=["quantity", "updated_at"])
    return cart


@transaction.atomic
def place_order(customer, address):
    cart = Cart.objects.select_for_update().prefetch_related("items__stock__medicine").get(customer=customer)
    items = list(cart.items.select_for_update().select_related("stock__medicine"))
    if not items:
        raise ValidationError("Your cart is empty.")
    for item in items:
        stock = item.stock
        if not stock.is_available or stock.quantity < item.quantity:
            raise ValidationError(f"{stock.medicine.name} is no longer available.")
    order = Order.objects.create(
        customer=customer, pharmacy=cart.pharmacy, address_snapshot=address,
        total=cart.total, payment_method="cod",
    )
    for item in items:
        stock = item.stock
        stock.quantity -= item.quantity
        stock.save(update_fields=["quantity", "updated_at"])
        OrderItem.objects.create(
            order=order, stock=stock, medicine_name=stock.medicine.name,
            price=stock.selling_price, quantity=item.quantity,
        )
    cart.items.all().delete()
    cart.pharmacy = None
    cart.save(update_fields=["pharmacy", "updated_at"])
    return order
