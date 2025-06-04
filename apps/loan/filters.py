from django.utils import choices
import django_filters

from django.db.models import Q
from apps.loan.models import Fine, Loan, Payment
from apps.profiles.models import Librarian
from core.filters import BaseFilter


class FineFilters(BaseFilter):
    status = django_filters.ChoiceFilter(
        field_name="payment__status", choices=Payment.STATUS_CHOICES
    )
    loan_status = django_filters.ChoiceFilter(field_name="loan__status", choices=Loan.STATUS_CHOICES)
    accepted_by = django_filters.ModelChoiceFilter(
        field_name="payment__accepted_by", queryset=Librarian.objects.all()
    )
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__iexact=value)
            | Q(loan__borrower__account__fullname__icontains=value)
            | Q(loan__borrower__id__iexact=value)
            | Q(loan__borrower__nis__iexact=value)
            | Q(loan__book__title__icontains=value)
            | Q(loan__book__id__iexact=value)
        )



    class Meta:
        model = Fine
        fields = ["status", "q", "accepted_by"]


class LoanFilters(BaseFilter):
    status = django_filters.ChoiceFilter(choices=Loan.STATUS_CHOICES)
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__iexact=value)
            | Q(borrower__account__fullname__icontains=value)
            | Q(borrower__id__iexact=value)
            | Q(borrower__nis__iexact=value)
            | Q(book__title__icontains=value)
            | Q(book__id__iexact=value)
        )


    class Meta:
        model = Loan
        fields = [
            "status",
            "q",
            "borrower",
            "book",
            "approved_by",
            "return_procced_by",
        ]
