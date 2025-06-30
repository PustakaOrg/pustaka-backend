from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.reservation.filters import ReservationFilters
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer
from apps.reservation.tasks import notify_reservation_ready_task

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

    def perform_update(self, serializer):
        instance = self.get_object()  
        old_status = instance.status
        updated = serializer.save() 
        new_status = updated.status

        if old_status == "pending" and new_status == "ready":
            notify_reservation_ready_task(updated.id)

