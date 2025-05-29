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
