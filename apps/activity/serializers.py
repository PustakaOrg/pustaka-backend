from rest_framework import serializers

from apps.activity.models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['action', 'message', 'created_at']
