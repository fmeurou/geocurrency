from datetime import datetime, timedelta
from django.core.cache import cache
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from iso4217 import Currency as Iso4217

from geocurrencies.countries.models import Country

BASE_CURRENCY = 'EUR'


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
    def all_currencies(cls):
        """
        Returns an array of currencies
        """
        return [Currency(c.code) for c in Iso4217]


    @classmethod
    def get_for_country(cls, alpha2):
        """
        Return a list of currencies for an alpha2 country code
        :params alpha2: alpha2 code of a country
        """
        try:
            country = Country(alpha2)
            return [Currency(cur) for cur in country.currencies()]
        except ValueError:
            return []

    def convert(self, target_currency, amount=1, conversion_date=None):
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
