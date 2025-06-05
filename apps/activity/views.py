from rest_framework import viewsets

from apps.activity.models import ActivityLog
from apps.activity.serializers import ActivityLogSerializer
from core.permissions import IsAdminOrLibrarianOnly

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminOrLibrarianOnly]

