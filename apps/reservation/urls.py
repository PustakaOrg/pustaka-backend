from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewset

router = DefaultRouter()
router.register(r"reservations",ReservationViewset)

urlpatterns = [
    path("",include(router.urls)),
]
