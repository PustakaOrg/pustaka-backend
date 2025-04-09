from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
