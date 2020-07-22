from countryinfo import CountryInfo
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from geocurrencies.helpers import service
from .models import Country
from .serializers import CountrySerializer, CountryDetailSerializer


class CountryViewset(ViewSet):
    """
    View for currency
    """

    def list(self, request):
        countries = Country.all_countries()
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            country = Country(pk)
            serializer = CountryDetailSerializer(country, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='timezones', url_name='timezones')
    def timezones(self, request, pk):
        """
        Send timezones for a specific country
        """
        try:
            c = Country(pk)
            return Response(c.timezones, content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='currencies', url_name='currencies')
    def currencies(self, request, pk):
        """
        Send timezones for a specific country
        """
        try:
            c = CountryInfo(pk)
            return Response(c.currencies(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='borders', url_name='borders')
    def borders(self, request, pk):
        """
        Send borders for a specific country
        """
        try:
            c = CountryInfo(pk)
            return Response(c.borders(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='provinces', url_name='provinces')
    def provinces(self, request, pk):
        """
        Send provinces for a specific country
        """
        try:
            c = CountryInfo(pk)
            return Response(c.provinces(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='languages', url_name='languages')
    def languages(self, request, pk):
        """
        Send languages for a specific country
        """
        try:
            c = CountryInfo(pk)
            return Response(c.languages(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @action(['GET'], detail=True, url_path='colors', url_name='colors')
    def colors(self, request, pk):
        """
            Get existing flag colors
        """
        try:
            return Response(Country(pk).colors(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    geocoder = openapi.Parameter('geocoder', openapi.IN_QUERY, description="Geocoder type", type=openapi.TYPE_STRING)
    geocoder_api_key = openapi.Parameter('geocoder_api_key', openapi.IN_QUERY, description="Geocoder API key",
                                         type=openapi.TYPE_STRING)
    address = openapi.Parameter('address', openapi.IN_QUERY, description="Address to look for",
                                type=openapi.TYPE_STRING)
    lat = openapi.Parameter('latitude', openapi.IN_QUERY, description="Latitude",
                            type=openapi.TYPE_STRING)
    lng = openapi.Parameter('longitude', openapi.IN_QUERY, description="Longitude",
                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', responses={200:openapi.TYPE_ARRAY})
    @action(['GET'], detail=False, url_path='geocoders', url_name='geocoders')
    def geocoders(self, request):
        """
        Return a list of available geocoders. As defined in settings.GEOCODING_SERVICE_SETTINGS
        """
        return Response(settings.SERVICES.get('geocoding', {}).keys(), content_type="application/json")

    @swagger_auto_schema(method='get', manual_parameters=[address, geocoder, geocoder_api_key])
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

    @swagger_auto_schema(method='get', manual_parameters=[lat, lng, geocoder, geocoder_api_key])
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
