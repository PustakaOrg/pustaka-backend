from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, PaymentViewSet, FineViewSet

router = DefaultRouter()
router.register(r"loans", LoanViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"fines", FineViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
