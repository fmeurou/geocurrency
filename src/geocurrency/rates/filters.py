from django_filters import rest_framework as filters
from .models import Rate


class RateFilter(filters.FilterSet):
    user = filters.BooleanFilter(label="filter rate associated to connected user")
    key = filters.CharFilter(label="filter rates with key", lookup_expr='exact',
                             method='key_filter')
    value_date = filters.DateFilter(label="filter rates at a specific date",
                                    field_name='value_date', lookup_expr='exact',
                                    method='key_filter')
    from_obj = filters.DateFilter(label="filter rates after a specific date (included)",
                                  field_name='value_date', lookup_expr='gte')
    to_obj = filters.DateFilter(label="filter rates before a specific date (included)",
                                field_name='value_date', lookup_expr='lte')
    value = filters.NumberFilter(label="filter rates with a specific value", field_name='value', lookup_expr='exact')
    lower_bound = filters.NumberFilter(label="filter rates with a value higher than the given value",
                                       field_name='value', lookup_expr='gte')
    higher_bound = filters.NumberFilter(label="filter rates with a value lower than the given value",
                                        field_name='value', lookup_expr='lte')
    currency = filters.CharFilter(label="filter by target currency", field_name='currency', lookup_expr='iexact')
    base_currency = filters.CharFilter(label="filter by base currency", field_name='base_currency', lookup_expr='iexact')

    class Meta:
        model = Rate
        fields = [
            'user', 'key',
            'value_date', 'from_obj', 'to_obj',
            'value', 'lower_bound', 'higher_bound',
            'currency', 'base_currency'
        ]

    def user_filter(self, queryset, name, value):
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
            })

    def key_filter(self, queryset, name, value):
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
                'key': value
            })