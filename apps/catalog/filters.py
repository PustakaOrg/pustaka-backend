import django_filters
from django.db.models import Q
from .models import Book, Category


class BookFilter(django_filters.FilterSet):
    category = django_filters.BaseInFilter(
        field_name="category__name",
        lookup_expr="in",
    )
    author = django_filters.CharFilter(
        field_name="author__fullname",
        lookup_expr="icontains",
        label="Author",
    )
    publisher = django_filters.CharFilter(
        field_name="publisher__name",
        lookup_expr="icontains",
        label="Publisher",
    )
    publisher_city = django_filters.CharFilter(
        field_name="publisher__city",
        lookup_expr="icontains",
        label="Publisher City",
    )
    shelf = django_filters.CharFilter(
        field_name="shelf__code",
        lookup_expr="icontains",
        label="Shelf",
    )
    publish_year = django_filters.RangeFilter()
    available = django_filters.BooleanFilter(method="filter_available")
    q = django_filters.CharFilter(method="filter_search")
    o = django_filters.OrderingFilter(
        fields=(
            ("shelf__code", "shelf"),
            ("publish_year", "publish_year"),
            ("title", "title"),
        )
    )

    class Meta:
        model = Book
        fields = [
            "q",
            "category",
            "author",
            "publisher",
            "publisher_city",
            "publish_year",
            "shelf",
            "available",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(isbn__iexact=value)
            | Q(title__icontains=value)
            | Q(id__iexact=value)  # for UUID match
        )

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(available_stock__gt=0)
        return queryset


class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

class PublisherFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))



class ShelfFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(code__icontains=value))


class AuthorFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(fullname__icontains=value))
