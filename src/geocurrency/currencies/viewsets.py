"""
Viewsets for currencies module APIs
"""

import logging
import statistics
from datetime import date, timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geocurrency.countries.serializers import CountrySerializer
from geocurrency.rates.serializers import RateSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Currency, CurrencyNotFoundError
from .serializers import CurrencySerializer


class CurrencyViewset(ReadOnlyModelViewSet):
    """
    View for currency
    """
    lookup_field = 'code'

    currencies_response = openapi.Response('List of currencies', CurrencySerializer)
    currency_response = openapi.Response('Currency detail', CurrencySerializer)
    ordering = openapi.Parameter('ordering', openapi.IN_QUERY,
                                 description="Sort on code, name, currency_name, "
                                             "exponent, number, value. "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[ordering, ], responses={200: currencies_response})
    def list(self, request, *args, **kwargs):
        """
        List of currencies
        """
        currencies = Currency.all_currencies(ordering=request.GET.get('ordering', 'name'))
        serializer = CurrencySerializer(currencies, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(responses={200: currency_response})
    def retrieve(self, request, code, *args, **kwargs) -> Response:
        """
        Retrieve single record based on iso4217 code
        """
        try:
            currency = Currency(code)
            serializer = CurrencySerializer(currency, context={'request': request})
            return Response(serializer.data)
        except CurrencyNotFoundError:
            return Response('Currency not found', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(method='get', responses={200: CountrySerializer})
    @action(['GET'], detail=True, url_path='countries', url_name="get_countries")
    def get_countries(self, request, code) -> Response:
        """
        Get all countries for the currency
        :param request: HTTP request
        :param code: Currency id
        :return: List of countries
        """
        try:
            currency = Currency(code)
            serializer = CountrySerializer(currency.countries,
                                           many=True,
                                           context={'request': request})
            return Response(serializer.data)
        except CurrencyNotFoundError as e:
            logging.error(e)
            return Response('Currency not found', status=status.HTTP_404_NOT_FOUND)

    from_date = openapi.Parameter('from_date', openapi.IN_QUERY,
                                  description="From date (YYYY-MM-DD)",
                                  type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY, description="To date (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING)
    base_currency = openapi.Parameter('base', openapi.IN_QUERY,
                                      description="Base currency (defaults to EUR)",
                                      type=openapi.TYPE_STRING)
    currency = openapi.Parameter('base_currency', openapi.IN_QUERY, description="currency",
                                 type=openapi.TYPE_STRING)
    key = openapi.Parameter('key', openapi.IN_QUERY, description="custom key",
                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get',
                         manual_parameters=[from_date, to_date, base_currency, key],
                         responses={200: RateSerializer})
    @action(['GET'], detail=True, url_path='rates', url_name="get_currency_rates")
    def get_rates(self, request, code: str,
                  key: str = None, base_currency: str = 'EUR',
                  from_date: date = date.today(), to_date: date = date.today()) -> Response:
        """
        Get conversion rates for the currency
        :param request: HTTP request
        :param code: Currency id
        :param key: optional custom key
        :param base_currency: optional base currency, defaults to EUR
        :param from_date: optional limit results to rates range in time
        :param to_date: optional limit results to rates range in time
        :return: List of rates
        """
        try:
            c = Currency(code)
            user = None
            if request.user and request.user.is_authenticated:
                user = request.user
            rates = c.get_rates(user=user, key=key, base_currency=base_currency,
                                start_date=from_date, end_date=to_date)
            serializer = RateSerializer(rates, many=True, context={'request': request})
            return Response(serializer.data)
        except CurrencyNotFoundError:
            return Response('Currency not found', status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_rates(
            base_currency: str,
            target_currency: str,
            from_date: date,
            to_date: date) -> dict:
        """
        Generates list of rates and stats
        :param base_currency: rate to currency
        :param target_currency: rate from currency
        :param from_date: lower date range
        :param to_date: higher date range
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
                    'currency': base_currency,
                    'reference': target_currency,
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
