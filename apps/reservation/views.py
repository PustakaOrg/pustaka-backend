from datetime import timedelta
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.activity.methods import log_activity
from apps.profiles.models import Librarian
from apps.loan.models import Loan  # adjust import as needed
from apps.loan.serializers import LoanSerializer  # if you have one
from rest_framework.exceptions import ValidationError

from apps.reservation.filters import ReservationFilters
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer
from apps.reservation.tasks import notify_reservation_ready_task


class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ReservationFilters

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()

        if request.user.groups.filter(name__in=["Member"]).exists():
            return queryset.filter(reservant__account=request.user)

        return super().get_queryset()

    def perform_create(self, serializer):
        reservant = serializer.validated_data.get("reservant")
        book = serializer.validated_data.get("book")

        existing_loan = Loan.objects.filter(
            borrower=reservant,
            book=book,
            status__in=["active", "overdue"],
        ).first()

        if existing_loan:
            raise ValidationError(
                {"detail": "Anda sudah meminjam buku ini."}
            )

        if reservant and book:
            has_active_reservation = Reservation.objects.filter(
                reservant=reservant,
                book=book,
                status__in=["pending", "ready"],
            ).exists()

            if has_active_reservation:
                raise ValidationError({"detail": "Anda sudah mereservasi buku ini."})

        if book.available_stock < 1:
            raise ValidationError({"detail": "Buku yang dipinjam kosong"})

        reservation = serializer.save()
        log_activity(
            "reserved",
            f"{reservation.reservant.account.fullname} mereservasi {reservation.book.title}",
        )
        book = reservation.book
        book.available_stock -= 1
        book.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        updated = serializer.save()
        new_status = updated.status

        if old_status == "pending" and new_status == "ready":
            notify_reservation_ready_task(updated.id)

    @action(detail=True, methods=["post"], url_path="convert-to-loan")
    def convert_to_loan(self, request, pk=None):
        reservation = self.get_object()

        existing_loan = Loan.objects.filter(
            borrower=reservation.reservant,
            book=reservation.book,
            status__in=["active", "overdue"],
        ).first()

        if existing_loan:
            return Response(
                {"detail": "This reservation already has an active or overdue loan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            librarian = Librarian.objects.get(account=request.user)
        except Librarian.DoesNotExist:
            raise PermissionDenied(
                {"detail": "Only librarians can perform this action."}
            )

        loan = Loan.objects.create(
            book=reservation.book,
            borrower=reservation.reservant,
            loan_date=reservation.pickup_date,
            return_date=reservation.pickup_date
            + timedelta(days=reservation.day_to_loan),
            approved_by=librarian,
            status="active",
        )

        log_activity(
            "borrowed", f"{loan.borrower.account.fullname} meminjam {loan.book.title}"
        )

        reservation.status = "completed"
        reservation.save()
        return Response(
            self.get_serializer(reservation).data, status=status.HTTP_201_CREATED
        )
