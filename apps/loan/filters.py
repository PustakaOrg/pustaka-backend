import django_filters

from apps.loan.models import Fine, Loan, Payment
from apps.profiles.models import Librarian


class FineFilters(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        field_name="payment__status", choices=Payment.STATUS_CHOICES
    )
    accepted_by = django_filters.ModelChoiceFilter(
        field_name="payment__accepted_by", queryset=Librarian.objects.all()
    )
    o = django_filters.OrderingFilter(fields=(("created_at", "created_at")))

    class Meta:
        model = Fine
        fields = ["status", "accepted_by"]


class LoanFilters(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Loan.STATUS_CHOICES)
    loan_date = django_filters.DateFromToRangeFilter()
    return_date = django_filters.DateFromToRangeFilter()
    o = django_filters.OrderingFilter(
        fields=(
            ("loan_date", "loan_date"),
            ("return_date", "return_date"),
        )
    )

    class Meta:
        model = Loan
        fields = [
            "status",
            "borrower",
            "loan_date",
            "return_date",
            "book",
            "approved_by",
            "return_procced_by",
        ]
