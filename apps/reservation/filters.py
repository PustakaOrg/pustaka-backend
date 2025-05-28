from django.db.models import Q
import django_filters

from apps.reservation.models import Reservation


class ReservationFilters(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Reservation.STATUS_CHOICES)
    reservation_date = django_filters.DateFromToRangeFilter()
    pickup_date = django_filters.DateFromToRangeFilter()
    q = django_filters.CharFilter(method="filter_search")
    o = django_filters.OrderingFilter(
        fields=(
            ("reservation_date", "reservation_date"),
            ("pickup_date", "pickup_date"),
        )
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__iexact=value)
            | Q(reservant__account__fullname__icontains=value)
            | Q(reservant__id__iexact=value)  
            | Q(reservant__nis__iexact=value) 
        )


    class Meta:
        model = Reservation
        fields = [
            "status",
            "reservation_date",
            "pickup_date",
            "reservant",
            "book",
            "accepted_by",
        ]
