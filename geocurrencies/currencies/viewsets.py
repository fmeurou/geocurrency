from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from geocurrencies.countries.serializers import CountrySerializer
from .filters import CurrencyFilter
from .models import CurrencyModel
from .permissions import CurrencyObjectPermission
from .serializers import CurrencySerializer


class CurrencyViewset(ReadOnlyModelViewSet):
    """
    View for currency
    """
    queryset = CurrencyModel.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = PageNumberPagination
    permission_classes = [CurrencyObjectPermission, ]
    display_page_controls = True
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CurrencyFilter

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super(CurrencyViewset, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super(CurrencyViewset, self).retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @action(['GET'], detail=True, url_path='countries', url_name="get_countries")
    def get_countries(self, request, pk, *args, **kwargs):
        """
        Get all countries for the currency
        :param pk: Currency id
        :return: List of countries
        """
        try:
            currency = CurrencyModel.objects.get(pk=pk)
            serializer = CountrySerializer(currency.countries, many=True, context={'request': request})
            return Response(serializer.data)

        except CurrencyModel.DoesNotExist:
            return HttpResponseNotFound('Currency not found')

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @action(['GET'], detail=True, url_path='rates', url_name="get_conversions")
    def get_rates(self, request, pk, *args, **kwargs):
        """
        Get conversion rates for the currency
        :param pk: Currency id
        :return: List of countries
        """
        if request.data.get('date'):
            pass

        if request.data.get('from_date'):
            pass


