from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.settings.urls")),
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.profiles.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/", include("apps.loan.urls")),
    path("api/", include("apps.reservation.urls")),
]
