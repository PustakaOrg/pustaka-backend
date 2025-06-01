import django_filters


class BaseFilter(django_filters.FilterSet):
    created_at_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte", label="Created At (From)"
    )
    created_at_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte", label="Created At (To)"
    )

    updated_at_from = django_filters.DateFilter(
        field_name="updated_at", lookup_expr="gte", label="Updated At (From)"
    )
    updated_at_to = django_filters.DateFilter(
        field_name="updated_at", lookup_expr="lte", label="Updated At (To)"
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('-created_at', 'created_at_desc'),
            ('updated_at', 'updated_at'),
            ('-updated_at', 'updated_at_desc'),
            ('id', 'id'),
            ('-id', 'id_desc'),
        ),
        field_labels={
            'created_at': 'Created At (ASC)',
            'created_at_desc': 'Created At (DESC)',
            'updated_at': 'Updated At (ASC)', 
            'updated_at_desc': 'Updated At (DESC)',
            'id': 'ID (ASC)',
            'id_desc': 'ID (DESC)',
        },
        label="Order By"
    )

    class Meta:
        abstract = True
