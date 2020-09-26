import logging
from datetime import date
from typing import Iterator

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from iso4217 import Currency as Iso4217

from geocurrency.countries.models import Country
from . import CURRENCY_SYMBOLS, DEFAULT_SYMBOL


class CurrencyNotFoundError(Exception):
    msg = 'Currency not found'


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
        try:
            i = Iso4217(code)
            for a in ['code', 'name', 'currency_name', 'exponent', 'number', 'value']:
                setattr(self, a, getattr(i, a))
        except ValueError:
            raise CurrencyNotFoundError('Invalid currency code')

    @classmethod
    def is_valid(cls, cur: str) -> bool:
        """
        Checks if currency is part of iso4217
        """
        try:
            Currency(cur)
            return True
        except CurrencyNotFoundError:
            return False

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
        except CurrencyNotFoundError as e:
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
        from geocurrency.rates.models import Rate
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

    @property
    def symbol(self):
        return CURRENCY_SYMBOLS.get(self.code, DEFAULT_SYMBOL)

