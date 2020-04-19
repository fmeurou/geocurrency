import requests
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from timezonefinder import TimezoneFinder

from .filters import CountryFilter
from .models import Country
from .permissions import CountryObjectPermission
from .serializers import CountrySerializer
from .settings import *

tf = TimezoneFinder(in_memory=True)


class CountryViewset(ReadOnlyModelViewSet):
    """
    View for currency
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = PageNumberPagination
    permission_classes = [CountryObjectPermission, ]
    display_page_controls = True
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CountryFilter

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super(CountryViewset, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super(CountryViewset, self).retrieve(request, *args, **kwargs)

    @action(['GET'], detail=True, url_path='timezones', url_name="get_timezones")
    def get_timezones(self, request, pk, *args, **kwargs):
        """
        Get all timezones for the country
        :param pk: Country id
        :return: List of timezones
        """
        try:
            country = Country.objects.get(pk=pk)
            return Response(country.timezones, content_type="application/json")
        except Country.DoesNotExist:
            return HttpResponseNotFound('Country not found')

    @action(['GET'], detail=False, url_path='geocode', url_name='geocoding')
    def geocode(self, request, *args, **kwargs):
        """
        Geocoding with Pelias
        """
        response = requests.get(PELIAS_API + 'search', {'text': request.GET.get('text')})
        data = response.json()
        countries = self.locations(data)
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @action(['GET'], detail=False, url_path='colors', url_name='colors')
    def colors(self, request, *args, **kwargs):
        """
            Get existing flag colors
        """
        _colors = []
        for country in Country.objects.all():
            if country.colors:
                _colors.extend(country.colors.split(','))
        return Response(sorted(list(set(_colors))), content_type="application/json")

    @action(['GET'], detail=False, url_path='reverse', url_name='reverse_geocoding')
    def reverse_geocode(self, request, *args, **kwargs):
        """
        Geocoding with Pelias
        """
        response = requests.get(PELIAS_API + 'reverse',
                                {
                                    'point.lat': request.GET.get('point.lat'),
                                    'point.lon': request.GET.get('point.lon')
                                })
        data = response.json()
        countries = self.locations(data)
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    def locations(self, data):
        """
        parse response from pelias service
        """
        alphas = {}
        countries = []
        for feature in data.get('features'):
            longitude, latitude = feature.get('geometry').get('coordinates')
            alphas[feature.get('properties').get('country_a')] = {
                'coordinates': feature.get('geometry').get('coordinates'),
                'timezone': tf.timezone_at(lng=longitude, lat=latitude)
            }
        for alpha, location in alphas.items():
            country = Country.objects.get(alpha_3=alpha)
            setattr(country, 'coordinates', location.get('coordinates', [0, 0]))
            setattr(country, 'timezone', location.get('timezone', ''))
            countries.append(country)
        return countries
