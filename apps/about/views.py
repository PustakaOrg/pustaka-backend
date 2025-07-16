from rest_framework import viewsets

from apps.about.serializers import AboutSerializer
from apps.about.models import About


class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

