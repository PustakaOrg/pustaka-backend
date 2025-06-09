from rest_framework import serializers

from apps.activity.methods import log_activity
from apps.catalog.models import Book
from apps.catalog.serializers import BookSerializer
from apps.profiles.serializers import LibrarianSerializer, MemberSerializer
from .models import Loan, Payment, Fine


class PopularBookSerializer(serializers.ModelSerializer):
    loan_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = [
            "id",
            # "img",
            "title",
            "isbn",
            # "author",
            "loan_count",
        ]  


class LoanSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """Customize the output representation."""
        representation = super().to_representation(instance)
        representation["borrower"] = MemberSerializer(
            instance.borrower, context=self.context
        ).data
        representation["book"] = BookSerializer(
            instance.book, context=self.context
        ).data
        representation["approved_by"] = None
        representation["return_procced_by"] = None
        if instance.approved_by is not None:
            representation["approved_by"] = LibrarianSerializer(
                instance.approved_by, context=self.context
            ).data
        if instance.return_procced_by is not None:
            representation["return_procced_by"] = LibrarianSerializer(
                instance.return_procced_by, context=self.context
            ).data
        return representation

    def create(self, validated_data):
        if validated_data["return_date"] < validated_data["loan_date"]:
            raise serializers.ValidationError("Return date must be after loan date.")
        book = validated_data["book"]

        if book.available_stock < 1:
            raise serializers.ValidationError(f"Book '{book.title}' is out of stock.")

        book.available_stock -= 1
        book.save()
        loan = super().create(validated_data)
        log_activity(
            "borrowed", f"{loan.borrower.account.fullname} meminjam {loan.book.title}"
        )

        return loan

    def update(self, instance, validated_data):
        book = validated_data.get("book", instance.book)
        previous_status = instance.status

        loan = super().update(instance, validated_data)

        if loan.status == "returned" and previous_status != "returned":
            book.available_stock += 1
            book.save()
            log_activity(
                "returned",
                f"{loan.borrower.account.fullname} mengembalikan {loan.book.title}",
            )

        if loan.status == "lost" and previous_status != "lost":
            book.stock -= 1
            book.save()

        return loan

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
            "created_at",
            "updated_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        original_status = instance.status
        payment = super().update(instance, validated_data)

        if original_status != "done" and payment.status == "done":
            loan = payment.fines.first().loan if payment.fines.exists() else None
            if loan:
                log_activity(
                    "payment_done",
                    f"Pembayaran Denda oleh {loan.borrower.account.fullname}",
                )
        return payment

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
        representation["payment"] = PaymentSerializer(
            instance.payment, context=self.context
        ).data
        representation["loan"] = LoanSerializer(
            instance.loan, context=self.context
        ).data
        return representation

    class Meta:
        model = Fine
        fields = ["id", "amount", "loan", "payment", "created_at", "updated_at"]
