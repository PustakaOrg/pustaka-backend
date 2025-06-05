from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.activity.views import ActivityLogViewSet

router = DefaultRouter()
router.register(r"activity-logs", ActivityLogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
