from rest_framework import serializers

from apps.catalog.serializers import BookSerializer
from apps.profiles.serializers import LibrarianSerializer, MemberSerializer
from .models import Loan, Payment, Fine


class LoanSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """Customize the output representation."""
        representation = super().to_representation(instance)
        representation["borrower"] = MemberSerializer(instance.borrower).data
        representation["book"] = BookSerializer(instance.book).data
        representation["approved_by"] = None
        representation["return_procced_by"] = None
        if instance.approved_by is not None:
            representation["approved_by"] = LibrarianSerializer(
                instance.approved_by
            ).data
        if instance.return_procced_by is not None:
            representation["return_procced_by"] = LibrarianSerializer(
                instance.return_procced_by
            ).data
        return representation

    def validate(self, data):
        if data["return_date"] < data["loan_date"]:
            raise serializers.ValidationError("Return date must be after loan date.")

        return data

    def create(self, validated_data):
        book = validated_data["book"]

        # Check availability before creating loan
        if book.available_stock < 1:
            raise serializers.ValidationError(f"Book '{book.title}' is out of stock.")
        
        # Deduct available stock and save the loan
        book.available_stock -= 1
        book.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        book = validated_data.get("book", instance.book)
        new_status = validated_data.get("status", instance.status)

        if new_status == "returned" and instance.status != "returned":
            book.available_stock += 1
            book.save()

        if new_status == "lost":
            book.stock -= 1
            book.save()

        # Proceed with updating the loan object
        return super().update(instance, validated_data)

    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_date",
            "return_date",
            "borrower",
            "book",
            "approved_by",
            "return_procced_by",
            "status",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "accepted_by",
            "status",
        ]


class FineSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["payment"] = PaymentSerializer(instance.payment).data
        return representation

    class Meta:
        model = Fine
        fields = [
            "id",
            "amount",
            "loan",
            "payment",
        ]
