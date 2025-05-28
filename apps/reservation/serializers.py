from rest_framework import serializers

from apps.catalog.models import Book
from apps.catalog.serializers import BookSerializer
from apps.profiles.serializers import LibrarianSerializer, MemberSerializer
from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["reservant"] = MemberSerializer(
            instance.reservant, context=self.context
        ).data
        representation["book"] = BookSerializer(
            instance.book, context=self.context
        ).data

        representation["accepted_by"] = None
        if instance.accepted_by is not None:
            representation["accepted_by"] = LibrarianSerializer(
                instance.accepted_by, context=self.context
            ).data

        return representation


    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)
        book = validated_data.get("book", instance.book)

        if new_status == "ready" and instance.status != "ready":
            book = Book.objects.select_for_update().get(pk=book.pk)
            if book.available_stock < 1:
                raise serializers.ValidationError(
                    f"Book '{book.title}' is out of stock."
                )
            book.save()

        return super().update(instance, validated_data)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "reservation_date",
            "pickup_date",
            "day_to_loan",
            "reservant",
            "book",
            "accepted_by",
            "status",
        ]
