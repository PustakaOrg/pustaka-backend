from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.about.views import AboutViewSet

router = DefaultRouter()
router.register(r'about', AboutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


