from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from core.settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.settings.urls")),
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.profiles.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/", include("apps.loan.urls")),
    path("api/", include("apps.reservation.urls")),
    path("api/", include("apps.dashboard.urls")),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
