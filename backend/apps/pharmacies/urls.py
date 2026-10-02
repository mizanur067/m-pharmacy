from rest_framework.routers import DefaultRouter
from .views import PharmacyViewSet

router = DefaultRouter()
router.register("", PharmacyViewSet, basename="pharmacy")
urlpatterns = router.urls
