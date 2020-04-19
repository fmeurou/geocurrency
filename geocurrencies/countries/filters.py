from django_filters import rest_framework as filters

from .models import Country


class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    capital = filters.CharFilter(field_name='capital', lookup_expr='icontains')
    region = filters.CharFilter(field_name='region', lookup_expr='icontains')
    subregion = filters.CharFilter(field_name='subregion', lookup_expr='icontains')
    color = filters.CharFilter(method='color_filter')

    def color_filter(self, queryset, name, value):
        return queryset & Country.objects.get_by_color(color=value)

    class Meta:
        model = Country
        fields = [
            'name',
            'alpha_2',
            'alpha_3',
            'capital',
            'continent',
            'region',
            'subregion',
            'dial',
            'color'
        ]
