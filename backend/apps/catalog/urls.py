from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ManufacturerViewSet, MedicineViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("manufacturers", ManufacturerViewSet, basename="manufacturer")
router.register("medicines", MedicineViewSet, basename="medicine")
urlpatterns = router.urls
