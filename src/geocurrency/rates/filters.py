from django.db import models
from django.db.models import OuterRef, Subquery
from django_filters import rest_framework as filters

from .models import Rate


class RateFilter(filters.FilterSet):
    user = filters.BooleanFilter(label="filter rate associated to connected user", method='user_filter')
    key = filters.CharFilter(label="filter rates with key", method='key_filter')
    value_date = filters.DateFilter(label="filter rates at a specific date",
                                    field_name='value_date', lookup_expr='exact')
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
    base_currency = filters.CharFilter(label="filter by base currency", field_name='base_currency',
                                       lookup_expr='iexact')
    currency_latest_values = filters.CharFilter(label="Only output latest rates for currency",
                                                method='currency_latest_values_filter')
    base_currency_latest_values = filters.CharFilter(label="Only output latest rates for currency",
                                                     method='base_currency_latest_values_filter')

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

    def currency_latest_values_filter(self, queryset, name, value):
        queryset = queryset.filter(currency=value)
        latest = queryset.filter(currency=OuterRef('currency')).order_by('-value_date')
        return queryset.annotate(
            currency_latest=Subquery(latest.values('value_date')[:1])
        ).filter(value_date=models.F('currency_latest'))

    def base_currency_latest_values_filter(self, queryset, name, value):
        queryset = queryset.filter(base_currency=value)
        latest = queryset.filter(base_currency=OuterRef('base_currency')).order_by('-value_date')
        return queryset.annotate(
            base_currency_latest=Subquery(latest.values('value_date')[:1])
        ).filter(value_date=models.F('base_currency_latest'))
