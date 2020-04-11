from django.http import HttpResponseNotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .filters import CountryFilter
from .models import Country
from .permissions import CountryObjectPermission
from .serializers import CountrySerializer


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

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
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