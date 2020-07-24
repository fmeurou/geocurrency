import statistics

import logging
from datetime import date, timedelta
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from geocurrencies.countries.serializers import CountrySerializer
from geocurrencies.rates.serializers import RateSerializer
from .models import Currency
from .serializers import CurrencySerializer


class CurrencyViewset(ReadOnlyModelViewSet):
    """
    View for currency
    """

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """
        List of currencies
        """
        currencies = Currency.all_currencies()
        serializer = CurrencySerializer(currencies, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, pk, *args, **kwargs) -> Response:
        """
        Retrieve single record
        """
        currency = Currency(pk)
        serializer = CurrencySerializer(currency, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: CountrySerializer})
    @action(['GET'], detail=True, url_path='countries', url_name="get_countries")
    def get_countries(self, request, pk) -> Response:
        """
        Get all countries for the currency
        :param request: HTTP request
        :param pk: Currency id
        :return: List of countries
        """
        try:
            currency = Currency(pk)
            serializer = CountrySerializer(currency.countries,
                                           many=True,
                                           context={'request': request})
            return Response(serializer.data)
        except (KeyError, ValueError) as e:
            logging.error(e)
            return HttpResponseNotFound('Currency not found')

    from_date = openapi.Parameter('from_date', openapi.IN_QUERY, description="From date (YYYY-MM-DD)",
                                  type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY, description="To date (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING)
    base_currency = openapi.Parameter('base', openapi.IN_QUERY, description="Base currency (defaults to EUR)",
                                      type=openapi.TYPE_STRING)
    currency = openapi.Parameter('base_currency', openapi.IN_QUERY, description="currency",
                                 type=openapi.TYPE_STRING)
    key = openapi.Parameter('key', openapi.IN_QUERY, description="custom key", type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get',
                         manual_parameters=[from_date, to_date, base_currency, key],
                         responses={200: RateSerializer})
    @action(['GET'], detail=True, url_path='rates', url_name="get_currency_rates")
    def get_rates(self, request, pk: str,
                  key: str = None, base_currency: str = 'EUR',
                  from_date: date = date.today(), to_date: date = date.today()) -> Response:
        """
        Get conversion rates for the currency
        :param request: HTTP request
        :param pk: Currency id
        :param key: optional custom key
        :param base_currency: optional base currency, defaults to EUR
        :param from_date: optional limit results to rates range in time
        :param to_date: optional limit results to rates range in time
        :return: List of rates
        """
        try:
            c = Currency(pk)
            user = None
            if request.user and request.user.is_authenticated:
                user = request.user
            rates = c.get_rates(user=user, key=key, base_currency=base_currency, start_date=from_date, end_date=to_date)
            serializer = RateSerializer(rates, many=True, context={'request': request})
            return Response(serializer.data)
        except Currency.DoesNotExist:
            return HttpResponseNotFound('Currency not found')

    def _get_rates(self, base_currency: str, target_currency: str, from_date: date, to_date: date) -> dict:
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
