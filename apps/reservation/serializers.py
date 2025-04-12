from rest_framework import serializers

from apps.catalog.serializers import BookSerializer
from apps.profiles.serializers import LibrarianSerializer, MemberSerializer
from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["reservant"] = MemberSerializer(instance.reservant).data
        representation["book"] = BookSerializer(instance.book).data
        representation["accepted_by"] = LibrarianSerializer(instance.accepted_by).data
        
        return representation

    class Meta:
        model = Reservation
        fields = [
            "id", 
            "reservation_date",
            "pickup_date",
            "reservant",
            "book",
            "accepted_by"
            "status"
        ]
