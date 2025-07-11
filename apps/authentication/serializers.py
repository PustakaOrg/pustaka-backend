from django.views.generic.dates import timezone_today
from rest_framework import serializers

from apps.authentication.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
# Import django packages
from django.utils.translation import gettext_lazy as _

# Import external packages
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as SimpleTokenObtainPairSerializer,
)




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
        representation["group"] = first_group.name if first_group else None
        return representation

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance

    class Meta:
        model = User
        fields = ["id", "fullname", "email", "password"]



class TokenObtainPairSerializer(SimpleTokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid Email or Password")}

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if hasattr(user, "member") and user.member.is_expired():
            raise serializers.ValidationError(
                {"detail": "Akun Anda telah kedaluwarsa."}
            )

        return data
