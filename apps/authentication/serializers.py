from rest_framework import serializers

from apps.authentication.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # def validate_password(self, value):
    #     try:
    #         django_validate_password(value)
    #     except DjangoValidationError as e:
    #         raise serializers.ValidationError(e.messages)
    #     return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        first_group = instance.groups.first()
        representation["group"] =  first_group.name if first_group else None
        return representation

    class Meta:
        model = User
        fields = ["id", "fullname", "email", "password"]
