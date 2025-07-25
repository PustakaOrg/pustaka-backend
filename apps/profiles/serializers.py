from django.core.exceptions import ValidationError
from apps.authentication.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apps.authentication.serializers import UserSerializer
from .models import Batch, Class, Member, Librarian


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["id", "name"]

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id", "name"]


class MemberSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    def create(self, validated_data):
        account_data = validated_data.pop("account")


        user = User.objects.create_member_user(
            fullname=account_data["fullname"],
            email=account_data["email"],
            password=account_data["password"],
        )

        member = Member.objects.create(**validated_data, account=user)

        return member

    def update(self, instance, validated_data):
        account_data = validated_data.pop("account", None)

        if account_data is not None:
            account = instance.account
            account.fullname = account_data.get("fullname", account.fullname)
            account.email = account_data.get("email", account.email)
            if "password" in account_data:
                account.password = make_password(account_data["password"])
            account.save()


        for attr, value in validated_data.items():
                setattr(instance, attr, value)

        instance.save()
        return instance


    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        single_fields = [
            ("_class", ClassSerializer),
            ("batch", BatchSerializer),
        ]

        for field, serializer in single_fields:
            value = getattr(instance, field, None)
            if value is not None:
                representation[field] = serializer(value).data

        return representation


    class Meta:
        model = Member
        fields = [
            "id",
            "profile_picture",
            "phone_number",
            "nis",
            "_class",
            "account",
            "batch",
            "expires_date"
        ]


class LibrarianSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    def create(self, validated_data):
        account_data = validated_data.pop("account")

        user = User.objects.create_librarian_user(
            fullname=account_data["fullname"],
            email=account_data["email"],
            password=account_data["password"],
        )

        librarian = Librarian.objects.create(**validated_data, account=user)
        return librarian

    def update(self, instance, validated_data):
        account_data = validated_data.pop("account", None)

        if account_data is not None:
            account = instance.account
            account.fullname = account_data.get("fullname", account.fullname)
            account.email = account_data.get("email", account.email)
            if "password" in account_data:
                account.password = make_password(account_data["password"])
            account.save()

        instance.nip = validated_data.get("nip", instance.nip)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.save()
        return instance

    class Meta:
        model = Librarian
        fields = ["id", "nip", "phone_number", "account"]
