from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.core.models import BaseModel
from apps.inventory.models import PharmacyStock
from apps.pharmacies.models import Pharmacy


class Cart(BaseModel):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.PROTECT, null=True, blank=True, related_name="carts")

    @property
    def total(self):
        return sum((item.line_total for item in self.items.select_related("stock")), Decimal("0"))


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    stock = models.ForeignKey(PharmacyStock, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=("cart", "stock"), name="unique_cart_stock")]

    @property
    def line_total(self):
        return self.stock.selling_price * self.quantity


class Order(BaseModel):
    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        CONFIRMED = "confirmed", "Confirmed"
        PACKED = "packed", "Packed"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    address_snapshot = models.TextField()
    payment_method = models.CharField(max_length=20, default="cod")
    total = models.DecimalField(max_digits=12, decimal_places=2)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    medicine_name = models.CharField(max_length=200)
    stock = models.ForeignKey(PharmacyStock, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
