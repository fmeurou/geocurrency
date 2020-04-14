from datetime import date, datetime, timedelta

from django.db import models
from django.core.cache import cache
from iso4217 import Currency
from pycountry import countries
from geocurrencies.countries.models import Country
from forex_python.converter import CurrencyRates

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

    @property
    def current_rate(self):
        yesterday = date.today() - timedelta(1)
        return self.rate(yesterday)

    def rate(self, conversion_date):
        try:
            return self.conversions.get(date=conversion_date).rate
        except ConversionRate.DoesNotExist:
            return None

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
            c = CurrencyRates()
            base_rate = c.convert(base_currency.code, self.code, 1, conversion_date)
        return conversion_date, base_currency, base_rate * amount


class ConversionRate(models.Model):
    currency = models.ForeignKey(CurrencyModel, related_name='conversions', on_delete=models.CASCADE)
    base_currency = models.ForeignKey(CurrencyModel, related_name='base_conversions', on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.FloatField()

    class Meta:
        unique_together = [['currency', 'base_currency', 'date']]


class CurrencyCountry(models.Model):
    currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)