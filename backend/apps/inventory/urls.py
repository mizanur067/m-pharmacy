from rest_framework.routers import DefaultRouter
from .views import PharmacyStockViewSet

router = DefaultRouter()
router.register("stocks", PharmacyStockViewSet, basename="stock")
urlpatterns = router.urls
