from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import TokenObtainPairView

from apps.authentication.views import UserViewset

router = DefaultRouter()
router.register(r"users", UserViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
