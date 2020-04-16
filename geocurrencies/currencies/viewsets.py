import statistics
from datetime import datetime, timedelta
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    date = openapi.Parameter('date', openapi.IN_QUERY, description="specific date", type=openapi.TYPE_STRING)
    from_date = openapi.Parameter('from_date', openapi.IN_QUERY, description="From date (YYYY-MM-DD)",
                                  type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY, description="To date (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING)
    reference = openapi.Parameter('reference', openapi.IN_QUERY, description="Reference currency (defaults to EUR)",
                                  type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', manual_parameters=[date, from_date, to_date, reference])
    @action(['GET'], detail=True, url_path='rates', url_name="get_conversions")
    def get_rates(self, request, pk, *args, **kwargs):
        """
        Get conversion rates for the currency
        :param pk: Currency id
        :return: List of countries
        """
        try:
            currency = CurrencyModel.objects.get(pk=pk)
        except CurrencyModel.DoesNotExist:
            return HttpResponseNotFound('Currency not found')
        try:
            reference = CurrencyModel.objects.get(pk=request.GET.get('reference', 'EUR'))
        except CurrencyModel.DoesNotExist:
            reference = CurrencyModel.objects.get(pk='EUR')
        dates = []
        rates = []
        stat = {}
        from_date = datetime.now()
        to_date = datetime.now()
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d')
        if request.GET.get('date'):
            from_date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
            to_date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
        for i in range((to_date - from_date).days + 1):
            d = from_date + timedelta(i)
            cd, reference, rate = currency.convert(
                base_currency=reference,
                conversion_date=d
            )
            rates.append(rate)
            dates.append(
                {
                    'conversion_date': cd.strftime('%Y-%m-%d'),
                    'currency': currency.code,
                    'reference': reference.code,
                    'rate': rate
                }
            )
        if len(rates) > 1:
            stat = {
                'avg': statistics.mean(rates),
                'median': statistics.median(rates),
                'max': max(rates),
                'min': min(rates),
                'std_deviation': statistics.stdev(rates)
            }
        return Response({'rates': dates, 'statistics': stat}, content_type="application/json")
