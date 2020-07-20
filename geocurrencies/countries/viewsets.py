from countryinfo import CountryInfo
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .models import Country
from .serializers import CountrySerializer
from ..geocoding.models import Geocoder


class CountryViewset(ViewSet):
    """
    View for currency
    """

    def list(self, request, *args, **kwargs):
        countries = Country.all_countries()
        serializer = CountrySerializer(countries, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            return Response(CountryInfo(pk).info(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True, url_path='timezones', url_name='timezones')
    def timezones(self, request, pk, *args, **kwargs):
        """
        Send timezones for a specific country
        """
        try:
            c = Country(pk)
            return Response(c.timezones, content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)


    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @action(['GET'], detail=True, url_path='colors', url_name='colors')
    def colors(self, request, pk, *args, **kwargs):
        """
            Get existing flag colors
        """
        try:
            return Response(Country(pk).colors(), content_type="application/json")
        except KeyError:
            return Response("Unknown country or no info for this country", status=HTTP_404_NOT_FOUND)

    address = openapi.Parameter('address', openapi.IN_QUERY, description="Address to look for",
                                type=openapi.TYPE_STRING)
    lat = openapi.Parameter('latitude', openapi.IN_QUERY, description="Latitude",
                            type=openapi.TYPE_STRING)
    lng = openapi.Parameter('longitude', openapi.IN_QUERY, description="Longitude",
                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', manual_parameters=[address])
    @action(['GET'], detail=False, url_path='geocode', url_name='geocoding')
    def geocode(self, request, *args, **kwargs):
        """
        Find country by geocoding (giving address or POI)
        """
        geocoder = Geocoder(key=request.GET.get('key'))
        data = geocoder.search(address=request.GET.get('address'))
        countries = geocoder.countries(data)
        return Response([c.base() for c in countries], content_type="application/json")

    @swagger_auto_schema(method='get', manual_parameters=[lat, lng])
    @action(['GET'], detail=False, url_path='reverse', url_name='reverse_geocoding')
    def reverse_geocode(self, request, *args, **kwargs):
        """
        Find country by reverse geocoding (giving latitude and longitude)
        """
        geocoder = Geocoder(key=request.GET.get('key'))
        data = geocoder.reverse(
            lat=request.GET.get('lat'),
            lng=request.GET.get('lon')
        )
        countries = geocoder.countries(data)
        return Response([c.base() for c in countries], content_type="application/json")
