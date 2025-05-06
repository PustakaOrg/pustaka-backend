import django_filters

from apps.loan.models import Loan


class LoanFilters(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Loan.STATUS_CHOICES)
    loan_date = django_filters.DateTimeFromToRangeFilter()
    return_date = django_filters.DateTimeFromToRangeFilter()
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
