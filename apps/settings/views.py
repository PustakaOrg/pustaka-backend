from rest_framework import generics
from rest_framework.response import Response

from core.permissions import IsAdmin, IsAdminModify
from .models import Settings
from .serializers import SettingsSerializer

class SettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = [IsAdminModify] 

    def get_object(self):
        return Settings.objects.get_instance()

    def update(self, request, *args, **kwargs):
        # Override to handle the update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
