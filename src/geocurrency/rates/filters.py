"""
REST filters for Rate APIs
"""

from django.db import models
from django.db.models import OuterRef, Subquery, QuerySet
from django_filters import rest_framework as filters

from .models import Rate


class RateFilter(filters.FilterSet):
    """
    Rate object filter
    """
    user = filters.BooleanFilter(label="filter rate associated to connected user",
                                 method='user_filter')
    key = filters.CharFilter(label="filter rates with key", method='key_filter')
    key_or_null = filters.CharFilter(label="filter rates with key or without key",
                                     method='key_or_null_filter')
    key_isnull = filters.CharFilter(label="filter rates without key", method='key_isnull_filter')
    value_date = filters.DateFilter(label="filter rates at a specific date",
                                    field_name='value_date', lookup_expr='exact')
    from_obj = filters.DateFilter(label="filter rates after a specific date (included)",
                                  field_name='value_date', lookup_expr='gte')
    to_obj = filters.DateFilter(label="filter rates before a specific date (included)",
                                field_name='value_date', lookup_expr='lte')
    value = filters.NumberFilter(label="filter rates with a specific value", field_name='value',
                                 lookup_expr='exact')
    lower_bound = filters.NumberFilter(
        label="filter rates with a value higher than the given value",
        field_name='value', lookup_expr='gte')
    higher_bound = filters.NumberFilter(
        label="filter rates with a value lower than the given value",
        field_name='value', lookup_expr='lte')
    currency = filters.CharFilter(label="filter by target currency", field_name='currency',
                                  lookup_expr='iexact')
    base_currency = filters.CharFilter(label="filter by base currency", field_name='base_currency',
                                       lookup_expr='iexact')
    currency_latest_values = filters.CharFilter(label="Only output latest rates for currency",
                                                method='currency_latest_values_filter')
    base_currency_latest_values = filters.CharFilter(label="Only output latest rates for currency",
                                                     method='base_currency_latest_values_filter')
    ordering = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('key', 'key'),
            ('value', 'value'),
            ('value_date', 'value_date'),
            ('base_currency', 'base_currency'),
            ('currency', 'currency'),
        ),
    )

    class Meta:
        """
        Meta
        """
        model = Rate
        exclude = ['pk', ]

    def user_filter(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on user
        """
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
            })
        return queryset.filter(user__isnull=True)

    def key_filter(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on key, only filters if request.user is set and authenticated
        """
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
                'key': value
            })
        return queryset.filter(user__isnull=True)

    def key_or_null_filter(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on key if user is authenticated or on records without user
        """
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(
                (models.Q(user=self.request.user) & models.Q(key=value)) | models.Q(
                    key__isnull=True)
            )
        return queryset.filter(user__isnull=True)

    @staticmethod
    def key_isnull_filter(queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on records without key
        """
        return queryset.filter(key__isnull=True)

    @staticmethod
    def currency_latest_values_filter(queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Returns a queryset of latest values fos a currency
        """
        queryset = queryset.filter(currency=value)
        latest = queryset.filter(currency=OuterRef('currency')).order_by('-value_date')
        return queryset.annotate(
            currency_latest=Subquery(latest.values('value_date')[:1])
        ).filter(value_date=models.F('currency_latest'))

    @staticmethod
    def base_currency_latest_values_filter(queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Returns a queryset of latest valeus for a base currency
        """
        queryset = queryset.filter(base_currency=value)
        latest = queryset.filter(base_currency=OuterRef('base_currency')).order_by('-value_date')
        return queryset.annotate(
            base_currency_latest=Subquery(latest.values('value_date')[:1])
        ).filter(value_date=models.F('base_currency_latest'))
