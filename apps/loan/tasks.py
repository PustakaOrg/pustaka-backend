from huey import crontab
from huey.contrib.djhuey import db_periodic_task
import random
import time

from apps.loan.methods import (
    add_fine_for_new_loans,
    create_overdue_message,
    create_return_day_reminder_message,
    get_current_overdue_loans,
    get_new_overdue_loans,
    get_today_return_day_loans,
    recalculate_overdue_fine,
)
from apps.notification.utils import send_wa


@db_periodic_task(crontab(hour="1"))
def process_new_ovedue_loan():
    new_overdue_loans = get_new_overdue_loans()
    if not new_overdue_loans:
        return
    add_fine_for_new_loans(new_overdue_loans)


@db_periodic_task(crontab(hour="5"))
def remind_return_loan():
    today_return_loans = get_today_return_day_loans()
    if not today_return_loans:
        return
    for loan in today_return_loans:
        delay = random.uniform(1, 10)
        time.sleep(delay)
        message = create_return_day_reminder_message(loan)
        send_wa(loan.borrower.phone_number, message)


@db_periodic_task(crontab(hour="6"))
def process_overdue_loan():
    overdue_loans = get_current_overdue_loans()
    if not overdue_loans:
        return
    recalculate_overdue_fine(overdue_loans)
    for overdue_loan in overdue_loans:
        delay = random.uniform(1, 10)
        time.sleep(delay)
        message = create_overdue_message(overdue_loan)
        send_wa(overdue_loan.borrower.phone_number, message)
