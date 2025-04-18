from django.core.exceptions import ValidationError
from apps.authentication.models import User
from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from .models import Class, Member, Librarian


# TODO: Updating this is still weird
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["id", "name"]


class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True, max_length=100)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["account"] = UserSerializer(instance.account).data
        return representation

    def create(self, validated_data):
        # Account Stuff
        email = validated_data.get("email")
        password = validated_data.get("password")
        fullname = validated_data.get("fullname")

        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        member_account = User.objects.create_member_user(
            password=password, email=email, fullname=fullname
        )

        # Member Stuff
        profile_picture = validated_data.get("profile_picture")
        phone_number = validated_data.get("phone_number")
        nis = validated_data.get("nis")
        # _class = validated_data.get("class")

        new_member = Member.objects.create(
            profile_picture=profile_picture,
            phone_number=phone_number,
            nis=nis,
            account=member_account,
            # _class=_class,
        )

        return new_member

    class Meta:
        model = Member
        fields = [
            "id",
            "profile_picture",
            "password",
            "email",
            "fullname",
            "phone_number",
            "nis",
            "class",
        ]


class LibrarianSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True, max_length=100)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["account"] = UserSerializer(instance.account).data
        return representation

    def create(self, validated_data):
        # Account Stuff
        email = validated_data.get("email")
        password = validated_data.get("password")
        fullname = validated_data.get("fullname")

        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        librarian_user = User.objects.create_librarian_user(password=password, email=email, fullname=fullname)
        phone_number = validated_data.get("phone_number")
        nip = validated_data.get("nip")

        new_librarian = Librarian.objects.create(nip=nip,phone_number=phone_number,account=librarian_user)
        return new_librarian



    class Meta:
        model = Librarian
        fields = ["id","email", "password", "fullname", "nip", "phone_number"]
