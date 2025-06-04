from django.db.models import Q
import django_filters

from apps.reservation.models import Reservation
from core.filters import BaseFilter


class ReservationFilters(BaseFilter):
    status = django_filters.ChoiceFilter(choices=Reservation.STATUS_CHOICES)
    reservation_date = django_filters.DateFromToRangeFilter()
    pickup_date = django_filters.DateFromToRangeFilter()
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__iexact=value)
            | Q(reservant__account__fullname__icontains=value)
            | Q(reservant__id__iexact=value)
            | Q(reservant__nis__iexact=value)
            | Q(book__title__icontains=value)
            | Q(book__id__iexact=value)
        )

    class Meta:
        model = Reservation
        fields = [
            "status",
            "q",
            "reservation_date",
            "pickup_date",
            "reservant",
            "book",
            "accepted_by",
        ]
