import logging
from datetime import date
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from iso4217 import Currency as Iso4217
from typing import Iterator

from geocurrencies.countries.models import Country
from geocurrencies.rates.models import Rate

BASE_CURRENCY = 'EUR'


class Currency:
    pass


class Currency:
    code = None
    name = None
    currency_name = None
    exponent = None
    number = 0
    value = None

    def __init__(self, code):
        """
        Returns a iso4217.Currency instance
        """
        i = Iso4217(code)
        for a in ['code', 'name', 'currency_name', 'exponent', 'number', 'value']:
            setattr(self, a, getattr(i, a))

    @classmethod
    def all_currencies(cls) -> Iterator[Currency]:
        """
        Returns an array of currencies
        """
        return [Currency(c.code) for c in Iso4217]

    @property
    def countries(self) -> Iterator[Country]:
        countries = []
        if cached_countries := cache.get(self.code + 'COUNTRIES'):
            return [Country(alpha_2) for alpha_2 in cached_countries]
        for country in Country.all_countries():
            try:
                if self.code in country.currencies():
                    countries.append(country)
            except KeyError:
                # Some countries listed in pycountry are not present in countryinfo
                pass
        cache.set(self.code + 'COUNTRIES', [country.alpha_2 for country in countries])
        return countries

    @classmethod
    def get_for_country(cls, alpha2: str) -> Iterator[Currency]:
        """
        Return a list of currencies for an alpha2 country code
        :params alpha2: alpha2 code of a country
        """
        try:
            country = Country(alpha2)
            return [Currency(cur) for cur in country.currencies()]
        except ValueError as e:
            logging.error("Error fetching currency")
            logging.error(e)
            return []

    def get_rates(self, user: User = None, key: str = None, base_currency: str = None, start_date: date = None,
                  end_date: date = None) -> Iterator:
        """
        Return a list of rates for this currency and an optional base currency between two dates
        :params base_currency: code of the base currency
        :params start_date: rates from that date included
        :params end_date: rates to that date included
        :return: List of rates
        """
        qs = Rate.objects.filter(currency=self.code)
        if user:
            qs = qs.filter(models.Q(user=user) | models.Q(user=None))
        if key:
            qs = qs.filter(key=key)
        if base_currency:
            qs = qs.filter(base_currency=base_currency)
        if start_date:
            qs = qs.filter(value_date__gte=start_date)
        if end_date:
            qs = qs.filter(value_date__lte=end_date)
        return qs

    def convert(self, client_key, target_currency, amount=1, conversion_date=None):
        if not conversion_date:
            conversion_date = datetime.now() - timedelta(1)
        cache_key = 'GEO{}{}{}'.format(
            conversion_date.strftime('%Y%m%d'),
            target_currency.code,
            self.code
        )
        base_rate = cache.get(cache_key)
        if not base_rate:
            try:
                c = CurrencyRates()
                base_rate = c.convert(target_currency.code, self.code, 1, conversion_date)
                cache.set(cache_key, base_rate, 60 * 60 * 24)
            except RatesNotAvailableError:
                base_rate = 0
        return conversion_date, target_currency, base_rate * amount
