import django_filters
from .models import  Book, Category


class BookFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="category__name",
        to_field_name="name",
        queryset=Category.objects.all(),
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
        if value:
            if value.isdigit() and len(value) in [10, 13]:
                # Exact match for ISBN
                return queryset.filter(isbn=value)
            else:
                return queryset.filter(title__icontains=value)

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(available_stock__gt=0)
        return queryset
