import django_filters
from .models import Batch, Class, Member
from django.db.models import Q


class MemberFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Search")
    batch = django_filters.UUIDFilter(field_name="batch")
    _class = django_filters.UUIDFilter(field_name="_class")

    class Meta:
        model = Member
        fields = ["q", "batch", "_class"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nis__iexact=value)
            | Q(account__fullname__icontains=value)
            | Q(id__iexact=value)  # for UUID match
        )


class ClassFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Class
        fields = ["q"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )


class BatchFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Batch
        fields = ["q"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )
