from apps.activity.models import ActivityLog


def log_activity(action: str, message: str):
    ActivityLog.objects.create(action=action, message=message)
