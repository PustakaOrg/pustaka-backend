import django_filters

from apps.reservation.models import Reservation


class ReservationFilters(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Reservation.STATUS_CHOICES)
    reservation_date = django_filters.DateFromToRangeFilter()
    pickup_date = django_filters.DateFromToRangeFilter()
    o = django_filters.OrderingFilter(
        fields=(
            ("reservation_date", "reservation_date"),
            ("pickup_date", "pickup_date"),
        )
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
