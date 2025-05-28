import django_filters
from .models import Member
from django.db.models import Q

class MemberFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Member
        fields = []

    def filter_search(self, queryset, name, value):
            return queryset.filter(
            Q(nis__iexact=value) |
            Q(account__fullname__icontains=value) |
            Q(id__iexact=value)  # for UUID match
        )
