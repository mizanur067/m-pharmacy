from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.inventory.models import PharmacyStock
from .models import Cart, Order
from .serializers import AddCartItemSerializer, CartSerializer, OrderSerializer, PlaceOrderSerializer
from .services import add_to_cart, place_order


class CartViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=("post",), url_path="items")
    def add_item(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock = PharmacyStock.objects.select_related("pharmacy", "medicine").filter(
            id=serializer.validated_data["stock"], is_active=True
        ).first()
        if not stock:
            from rest_framework.exceptions import NotFound
            raise NotFound("Stock item was not found.")
        cart = add_to_cart(request.user, stock, serializer.validated_data["quantity"])
        cart = Cart.objects.prefetch_related("items__stock__medicine", "items__stock__pharmacy").get(id=cart.id)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=("delete",), url_path="items/(?P<item_id>[^/.]+)")
    def remove_item(self, request, item_id=None):
        cart = Cart.objects.filter(customer=request.user).first()
        if cart:
            cart.items.filter(id=item_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related("items").order_by("-created_at")

    @action(detail=False, methods=("post",), url_path="place")
    def place(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = place_order(request.user, serializer.validated_data["address"])
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
