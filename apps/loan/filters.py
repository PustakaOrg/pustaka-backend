import django_filters

from apps.loan.models import Fine, Loan, Payment
from apps.profiles.models import Librarian
from core.filters import BaseFilter


class FineFilters(BaseFilter):
    status = django_filters.ChoiceFilter(
        field_name="payment__status", choices=Payment.STATUS_CHOICES
    )
    accepted_by = django_filters.ModelChoiceFilter(
        field_name="payment__accepted_by", queryset=Librarian.objects.all()
    )

    class Meta:
        model = Fine
        fields = ["status", "accepted_by"]


class LoanFilters(BaseFilter):
    status = django_filters.ChoiceFilter(choices=Loan.STATUS_CHOICES)


    class Meta:
        model = Loan
        fields = [
            "status",
            "borrower",
            "book",
            "approved_by",
            "return_procced_by",
        ]
