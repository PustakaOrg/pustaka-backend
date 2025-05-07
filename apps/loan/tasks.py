from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from apps.loan.methods import add_fine_for_new_loans, get_current_overdue_loans, get_new_overdue_loans, recalculate_overdue_fine


@db_periodic_task(crontab(hour="1"))
def process_new_ovedue_loan():
    new_overdue_loans = get_new_overdue_loans()
    add_fine_for_new_loans(new_overdue_loans)



@db_periodic_task(crontab(hour="2"))
def process_overdue_loan():
    overdue_loans = get_current_overdue_loans()
    recalculate_overdue_fine(overdue_loans)
