from apps.loan.message import OVERDUE_FINED_MESSAGE, RETURN_DAY_REMINDER_MESSAGE
from apps.loan.models import Fine, Loan, Payment
from django.utils import timezone

from django.db import transaction

from apps.settings.models import Settings


def create_overdue_message(loan: Loan):
    overdue_msg = OVERDUE_FINED_MESSAGE.format(
        borrower_name=loan.borrower.account.fullname,
        book_title=loan.book.title,
        fine_amount=loan.fines.amount,
    )
    return overdue_msg


def create_return_day_reminder_message(loan: Loan):
    reminder_msg = RETURN_DAY_REMINDER_MESSAGE.format(
        borrower_name=loan.borrower.account.fullname,
        book_title=loan.book.title,
    )
    return reminder_msg


def get_new_overdue_loans():
    current_date = timezone.now()
    new_overdue_loans = Loan.objects.filter(
        status="active", return_date__lt=current_date
    )
    for new_overdue_loan in new_overdue_loans:
        new_overdue_loan.status = "overdue"
        new_overdue_loan.save()
    return new_overdue_loans


def add_fine_for_new_loans(new_overdue_loans):
    late_fine_amount = Settings.objects.get_instance().fine_per_lateday
    for new_overdue_loan in new_overdue_loans:
        with transaction.atomic():
            payment = Payment()
            payment.save()
            fine = Fine(amount=late_fine_amount, loan=new_overdue_loan, payment=payment)
            fine.save()


def get_current_overdue_loans():
    return Loan.objects.filter(status="overdue")


def get_today_return_day_loans():
    today = timezone.now().date()
    return Loan.objects.filter(return_date=today)


def recalculate_overdue_fine(overdue_loans):
    current_date = timezone.now().date()
    late_fine_amount = Settings.objects.get_instance().fine_per_lateday
    for overdue_loan in overdue_loans:
        late_days = (current_date - overdue_loan.return_date).days
        new_fine_amount = late_days * late_fine_amount
        fine = overdue_loan.fines
        fine.amount = new_fine_amount
        fine.save()
