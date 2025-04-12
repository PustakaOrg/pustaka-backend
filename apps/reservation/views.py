from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer

class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes  = [IsAuthenticated]

