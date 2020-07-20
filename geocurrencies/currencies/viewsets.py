import statistics
from datetime import datetime, timedelta
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from geocurrencies.countries.models import Country
from geocurrencies.countries.serializers import CountrySerializer
from .models import Currency
from .serializers import CurrencySerializer


class CurrencyViewset(ReadOnlyModelViewSet):
    """
    View for currency
    """

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        currencies = Currency.all_currencies()
        serializer = CurrencySerializer(currencies, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, pk, *args, **kwargs):
        currency = Currency(pk)
        serializer = CurrencySerializer(currency, context={'request': request})
        return Response(serializer.data)

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
            currency = Currency(pk)
            serializer = CountrySerializer(
                [Country(c) for c in currency.countries],
                many=True,
                context={'request': request})
            return Response(serializer.data)
        except KeyError:
            return HttpResponseNotFound('Currency not found')

    from_date = openapi.Parameter('from_date', openapi.IN_QUERY, description="From date (YYYY-MM-DD)",
                                  type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY, description="To date (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING)
    base = openapi.Parameter('base', openapi.IN_QUERY, description="Base currency (defaults to EUR)",
                               type=openapi.TYPE_STRING)
    target = openapi.Parameter('target', openapi.IN_QUERY, description="Target currency (defaults to EUR)",
                                  type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', manual_parameters=[from_date, to_date, target])
    @action(['GET'], detail=True, url_path='rates', url_name="get_currency_rates")
    def get_currency_rates(self, request, pk, *args, **kwargs):
        """
        Get conversion rates for the currency
        :param pk: Currency id
        :return: List of countries
        """
        try:
            base_currency = CurrencyModel.objects.get(pk=pk)
        except CurrencyModel.DoesNotExist:
            return HttpResponseNotFound('Currency not found')
        try:
            target_currency = CurrencyModel.objects.get(pk=request.GET.get('target', 'EUR'))
        except CurrencyModel.DoesNotExist:
            target_currency = CurrencyModel.objects.get(pk='EUR')
        from_date = datetime.now()
        to_date = datetime.now()
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d')
        return Response(self._get_rates(
            base_currency=base_currency,
            target_currency=target_currency,
            from_date=from_date,
            to_date=to_date
        ), content_type="application/json")

    @swagger_auto_schema(method='get', manual_parameters=[from_date, to_date, base, target])
    @action(['GET'], detail=False, url_path='rates', url_name="get_conversions")
    def get_rates(self, request, *args, **kwargs):
        """
        Get conversion rates between two currencies
        :param pk: Currency id
        :return: List of conversion rates
        """
        try:
            base_currency = CurrencyModel.objects.get(pk=request.GET.get('base', 'EUR'))
        except CurrencyModel.DoesNotExist:
            base_currency = CurrencyModel.objects.get(pk='EUR')
        try:
            target_currency = CurrencyModel.objects.get(pk=request.GET.get('target', 'EUR'))
        except CurrencyModel.DoesNotExist:
            target_currency = CurrencyModel.objects.get(pk='EUR')
        from_date = datetime.now()
        to_date = datetime.now()
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d')

        return Response(self._get_rates(
            base_currency=base_currency,
            target_currency=target_currency,
            from_date=from_date,
            to_date=to_date
        ), content_type="application/json")

    def _get_rates(self, base_currency, target_currency, from_date, to_date):
        """
        Generates list of rates and stats
        """
        rates = []
        dates = []
        for i in range((to_date - from_date).days + 1):
            d = from_date + timedelta(i)
            cd, reference, rate = base_currency.convert(
                target_currency=target_currency,
                conversion_date=d
            )
            rates.append(rate)
            dates.append(
                {
                    'conversion_date': cd.strftime('%Y-%m-%d'),
                    'currency': base_currency.code,
                    'reference': target_currency.code,
                    'rate': rate
                }
            )
        stat = {}
        if len(rates) > 1:
            stat = {
                'avg': statistics.mean(rates),
                'median': statistics.median(rates),
                'max': max(rates),
                'min': min(rates),
                'std_deviation': statistics.stdev(rates)
            }
        return {'rates': dates, 'statistics': stat}
