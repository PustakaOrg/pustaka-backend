from rest_framework import serializers

from apps.authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "fullname", "email", "password"]
