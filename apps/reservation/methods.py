from django.utils import timezone
from django.db.models import Q
from apps.notification.utils import send_wa
from apps.reservation.messages import (
    RESERVATION_EXPIRED_MESSAGE,
    RESERVATION_READY_MESSAGE,
)
from apps.reservation.models import Reservation


def create_expired_reservation_message(reservation):
    return RESERVATION_EXPIRED_MESSAGE.format(
        reservant=reservation.reservant.account.fullname,
        book_title=reservation.book.title,
    )


def notify_reservation_ready(reservation):
    if reservation.reservant.phone_number:
        message = RESERVATION_READY_MESSAGE.format(
            reservant=reservation.reservant.account.fullname,
            book_title=reservation.book.title,
        )
        send_wa(
            recepiant=reservation.reservant.phone_number,
            message=message,
        )


def proccess_expired_reservations():
    current_date = timezone.now()
    new_expired_reservations = Reservation.objects.filter(
        Q(status="pending") | Q(status="ready"), pickup_date__lt=current_date
    )
    for new_expired_reservation in new_expired_reservations:
        new_expired_reservation.status = "expired"
        new_expired_reservation.save()

        if new_expired_reservation.reservant.phone_number:
            message = create_expired_reservation_message(new_expired_reservation)
            send_wa(
                recepiant=new_expired_reservation.reservant.phone_number,
                message=message,
            )
    return new_expired_reservations
