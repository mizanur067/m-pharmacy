from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import OwnerDashboardView, PharmacyViewSet

router = DefaultRouter()
router.register("", PharmacyViewSet, basename="pharmacy")
urlpatterns = [path("dashboard/", OwnerDashboardView.as_view(), name="owner-dashboard"), *router.urls]
