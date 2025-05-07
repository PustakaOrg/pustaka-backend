from apps.loan.models import Fine, Loan, Payment
from django.utils import timezone

from apps.settings.models import Settings


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
        payment = Payment()
        payment.save()
        fine = Fine(amount=late_fine_amount, loan=new_overdue_loan, payment=Payment())
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
        fine = overdue_loan.fines.get()
        fine.amount = new_fine_amount
        fine.save()
