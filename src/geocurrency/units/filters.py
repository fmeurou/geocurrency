"""
Units module API filters
"""

from django.db import models
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from .models import CustomUnit


class CustomUnitFilter(filters.FilterSet):
    """
    Filter on custom units
    """
    user = filters.BooleanFilter(label="filter rate associated to connected user",
                                 method='user_filter')
    key = filters.CharFilter(label="filter rates with key", method='key_filter')
    unit_system = filters.CharFilter(label="filter by unit system", field_name='unit_system',
                                     lookup_expr='iexact')
    code = filters.CharFilter(label="filter by code", field_name='code', lookup_expr='iexact')
    name = filters.CharFilter(label="filter by name", field_name='name', lookup_expr='icontains')
    relation = filters.CharFilter(label="filter by relation", field_name='relation',
                                  lookup_expr='icontains')
    symbol = filters.CharFilter(label="filter by symbol", field_name='symbol', lookup_expr='iexact')
    alias = models.CharField("Alias", max_length=20, null=True, blank=True)

    ordering = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('key', 'key'),
            ('unit_system', 'unit_system'),
            ('code', 'code'),
            ('name', 'name'),
            ('relation', 'relation'),
            ('symbol', 'symbol'),
            ('alias', 'alias'),
        ),
    )

    class Meta:
        """
        Meta
        """
        model = CustomUnit
        fields = [
            'user', 'key',
            'unit_system', 'code', 'name',
            'relation', 'symbol', 'alias'

        ]

    def user_filter(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on request user
        """
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
            })
        return queryset.filter(user__isnull=True)

    def key_filter(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filter on key if request.user is set and authenticated
        """
        if self.request and self.request.user and self.request.user.is_authenticated:
            return queryset.filter(**{
                'user': self.request.user,
                'key': value
            })
        return queryset.filter(user__isnull=True)
