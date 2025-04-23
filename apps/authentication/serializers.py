from rest_framework import serializers

from apps.authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        first_group = instance.groups.first()
        representation["group"] =  first_group.name if first_group else None
        return representation

    class Meta:
        model = User
        fields = ["id", "fullname", "email", "password"]
