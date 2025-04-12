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
        representation["approved_by"] = LibrarianSerializer(instance.approved_by).data
        representation["return_processed_by"] = LibrarianSerializer(
            instance.return_processed_by
        ).data
        return representation

    def validate(self, data):
        if data["return_date"] < data["loan_date"]:
            raise serializers.ValidationError("Return date must be after loan date.")
        return data

    class Meta:
        model = Loan
        fields = [
            "id",  # Assuming you have an ID field in BaseModel
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
            "id",  # Assuming you have an ID field in BaseModel
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
            "id",  # Assuming you have an ID field in BaseModel
            "amount",
            "loan",
            "payment",
        ]
