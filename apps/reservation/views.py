from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.reservation.filters import ReservationFilters
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer

class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes  = [IsAuthenticated]
    filterset_class = ReservationFilters

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()

        if request.user.groups.filter(name__in=["Member"]).exists():
            return queryset.filter(reservant__account=request.user)

        return super().get_queryset()

