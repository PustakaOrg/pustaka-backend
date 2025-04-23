from django.urls import path

from apps.notification.views import (
    check_status_view,
    disconnect_view,
    get_qr_view,
    profile_view,
)

urlpatterns = [
    path("wa/status/", check_status_view, name="wa-check-status"),
    path("wa/qr/", get_qr_view, name="wa-qr"),
    path("wa/disconnect", disconnect_view, name="wa-disconnect"),
    path("wa/profile", profile_view, name="wa-profile"),
]
