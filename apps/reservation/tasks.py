from apps.reservation.methods import notify_reservation_ready, proccess_expired_reservations
from apps.reservation.models import Reservation
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task
#
#
@db_periodic_task(crontab(hour="7", minute="0"))
def process_expired_reservation_task():
    proccess_expired_reservations()

@db_task()
def notify_reservation_ready_task(reservation_id):
    reservation = Reservation.objects.select_related(
                "reservant__account", "book"
            ).get(id=reservation_id)
    notify_reservation_ready(reservation)
