from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="stock.medicine.name", read_only=True)
    pharmacy_name = serializers.CharField(source="stock.pharmacy.name", read_only=True)
    unit_price = serializers.DecimalField(source="stock.selling_price", max_digits=10, decimal_places=2, read_only=True)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "stock", "medicine_name", "pharmacy_name", "quantity", "unit_price", "line_total")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "pharmacy", "items", "total")


class AddCartItemSerializer(serializers.Serializer):
    stock = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, max_value=100)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "medicine_name", "price", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "pharmacy", "status", "address_snapshot", "payment_method", "total", "items", "created_at")


class PlaceOrderSerializer(serializers.Serializer):
    address = serializers.CharField(min_length=5, max_length=1000)
