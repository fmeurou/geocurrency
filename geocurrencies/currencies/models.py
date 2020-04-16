from datetime import date, datetime, timedelta

from django.db import models
from django.core.cache import cache
from iso4217 import Currency
from pycountry import countries
from geocurrencies.countries.models import Country
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError

BASE_CURRENCY = 'EUR'


class CurrencyManager(models.Manager):

    def filter_by_country(self, country):
        try:
            country = countries.lookup(country)
        except LookupError:
            return None
        codes = [cur.code for cur in
                 [cur for cur in Currency if country.name.lower() in map(str.lower, cur.country_names)]
                 ]
        return CurrencyModel.objects.filter(code__in=codes)


class CurrencyModel(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    numeric = models.IntegerField()
    name = models.CharField(max_length=255)
    exponent = models.IntegerField()
    countries = models.ManyToManyField(Country, related_name='currencies', through="CurrencyCountry")
    objects = CurrencyManager()

    def convert(self, base_currency, amount=1, conversion_date=None):
        if not conversion_date:
            conversion_date = datetime.now() - timedelta(1)
        cache_key = 'GEO{}{}{}'.format(
            conversion_date.strftime('%Y%m%d'),
            base_currency.code,
            self.code
        )
        base_rate = cache.get(cache_key)
        if not base_rate:
            try:
                c = CurrencyRates()
                base_rate = c.convert(base_currency.code, self.code, 1, conversion_date)
                cache.set(cache_key, base_rate, 60*60*24)
            except RatesNotAvailableError:
                base_rate = 0
        return conversion_date, base_currency, base_rate * amount


class CurrencyCountry(models.Model):
    currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)