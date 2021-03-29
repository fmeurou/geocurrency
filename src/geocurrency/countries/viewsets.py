"""
Country API viewsets
"""

from countryinfo import CountryInfo
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geocurrency.core.helpers import service
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .models import Country, CountryNotFoundError
from .serializers import CountrySerializer, CountryDetailSerializer


class CountryViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'alpha_2'

    language_header = openapi.Parameter('Accept-Language', openapi.IN_HEADER,
                                        description="language",
                                        type=openapi.TYPE_STRING)
    language = openapi.Parameter('language', openapi.IN_QUERY, description="language",
                                 type=openapi.TYPE_STRING)
    ordering = openapi.Parameter('ordering', openapi.IN_QUERY,
                                 description="Sort on name, alpha_2, alpha_3, numeric. "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    countries_response = openapi.Response('List of countries', CountrySerializer)
    country_detail_response = openapi.Response('Country detail', CountryDetailSerializer)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header, ordering],
                         responses={200: countries_response})
    def list(self, request):
        """
        List countries. this view is not paginated
        """
        countries = Country.all_countries(ordering=request.GET.get('ordering', 'name'))
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header],
                         responses={200: country_detail_response})
    def retrieve(self, request, alpha_2: str):
        """
        Retrieve a Country based on its alpha 2 code
        """
        try:
            country = Country(alpha_2)
            serializer = CountryDetailSerializer(country, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except CountryNotFoundError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='timezones', url_name='timezones')
    def timezones(self, request, alpha_2):
        """
        Send timezones for a specific country
        """
        try:
            c = Country(alpha_2)
            return Response(c.timezones, content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='currencies', url_name='currencies')
    def currencies(self, request, alpha_2):
        """
        Send timezones for a specific country
        """
        try:
            c = CountryInfo(alpha_2)
            return Response(c.currencies(), content_type="application/json")
        except KeyError:
            return Response(_("Unknown country or no info for this country"),
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='borders', url_name='borders')
    def borders(self, request, alpha_2):
        """
        Send borders for a specific country
        """
        try:
            c = CountryInfo(alpha_2)
            return Response(c.borders(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='provinces', url_name='provinces')
    def provinces(self, request, alpha_2):
        """
        Send provinces for a specific country
        """
        try:
            c = CountryInfo(alpha_2)
            return Response(c.provinces(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='languages', url_name='languages')
    def languages(self, request, alpha_2):
        """
        Send languages for a specific country
        """
        try:
            c = CountryInfo(alpha_2)
            return Response(c.languages(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=True, url_path='colors', url_name='colors')
    def colors(self, request, alpha_2):
        """
            Get existing flag colors
        """
        try:
            c = Country(alpha_2=alpha_2)
            return Response(c.colors(), content_type="application/json")
        except CountryNotFoundError:
            return Response("Unknown country or no info for this country",
                            status=HTTP_404_NOT_FOUND)

    geocoder = openapi.Parameter('geocoder', openapi.IN_QUERY, description="Geocoder type",
                                 type=openapi.TYPE_STRING)
    geocoder_api_key = openapi.Parameter('geocoder_api_key', openapi.IN_QUERY,
                                         description="Geocoder API key",
                                         type=openapi.TYPE_STRING)
    address = openapi.Parameter('address', openapi.IN_QUERY, description="Address to look for",
                                type=openapi.TYPE_STRING)
    lat = openapi.Parameter('latitude', openapi.IN_QUERY, description="Latitude",
                            type=openapi.TYPE_STRING)
    lng = openapi.Parameter('longitude', openapi.IN_QUERY, description="Longitude",
                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', responses={200: openapi.TYPE_ARRAY})
    @action(['GET'], detail=False, url_path='geocoders', url_name='geocoders')
    def geocoders(self, request):
        """
        Return a list of available geocoders. As defined in settings.GEOCODING_SERVICE_SETTINGS
        """
        return Response(settings.SERVICES.get('geocoding', {}).keys(),
                        content_type="application/json")

    @swagger_auto_schema(method='get', manual_parameters=[address, geocoder, geocoder_api_key],
                         responses={200: CountrySerializer})
    @action(['GET'], detail=False, url_path='geocode', url_name='geocoding')
    def geocode(self, request):
        """
        Find country by geocoding (giving address or POI)
        """
        geocoder = service(service_type='geocoding',
                           service_name=request.GET.get('geocoder', settings.GEOCODING_SERVICE),
                           key=request.GET.get('geocoder_api_key', settings.GEOCODER_GOOGLE_KEY))
        data = geocoder.search(address=request.GET.get('address'))
        countries = geocoder.countries(data)
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(method='get', manual_parameters=[lat, lng, geocoder, geocoder_api_key],
                         responses={200: CountrySerializer})
    @action(['GET'], detail=False, url_path='reverse', url_name='reverse_geocoding')
    def reverse_geocode(self, request):
        """
        Find country by reverse geocoding (giving latitude and longitude)
        """
        geocoder = service(service_type='geocoding',
                           service_name=request.GET.get('geocoder', settings.GEOCODING_SERVICE),
                           key=request.GET.get('geocoder_api_key', settings.GEOCODER_GOOGLE_KEY))
        data = geocoder.reverse(
            lat=request.GET.get('lat'),
            lng=request.GET.get('lon')
        )
        countries = geocoder.countries(data)
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)
