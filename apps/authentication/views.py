from django.shortcuts import render
from rest_framework import viewsets

from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from core.permissions import IsAdmin

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
