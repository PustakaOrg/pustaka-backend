from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.notification.utils import check_status, disconnect, get_profile, get_qr_code
from core.permissions import IsAdmin


@api_view(["GET"])
@permission_classes([IsAdmin])
def check_status_view(request):
    status = check_status()
    return Response({"status": status})

@api_view(["GET"])
@permission_classes([IsAdmin])
def get_qr_view(request):
    qrcode_raw = get_qr_code()
    return Response({"qrcode_raw": qrcode_raw})

@api_view(["GET"])
@permission_classes([IsAdmin])
def disconnect_view(request):
    disconnect()
    return Response({"disconnected": "true"})

@api_view(["GET"])
@permission_classes([IsAdmin])
def profile_view(request):
    profile = get_profile()
    return Response(profile)
