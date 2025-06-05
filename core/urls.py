from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from core.settings import DEBUG

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.settings.urls")),
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.profiles.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/", include("apps.loan.urls")),
    path("api/", include("apps.reservation.urls")),
    path("api/", include("apps.dashboard.urls")),
    path("api/", include("apps.activity.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include("apps.notification.urls")),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
