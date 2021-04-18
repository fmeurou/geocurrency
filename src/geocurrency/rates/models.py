"""
Models for Rates module
"""
from datetime import date, timedelta

import networkx as nx
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from geocurrency.converters.models import BaseConverter, ConverterResult, ConverterResultDetail, \
    ConverterResultError
from geocurrency.core.helpers import service

try:
    RATE_SERVICE = settings.RATE_SERVICE
except AttributeError:
    pass

from .services import RatesNotAvailableError


class NoRateFound(Exception):
    """
    Exception when no rate is found
    """
    pass


class BaseRate(models.Model):
    """
    Just an abstract for value and hinting
    """
    value = None

    class Meta:
        """
        Yes, it is abstract
        """
        abstract = True


class RateManager(models.Manager):
    """
    Manager for Rate model
    """

    @staticmethod
    def __sync_rates__(rates: [], base_currency: str):
        """
        Sync rates to the database
        :param rates: array of dict of rates from service
        :param base_currency: base currency to fetch
        """
        output = []
        for rate in rates:
            _rate, created = Rate.objects.get_or_create(
                base_currency=base_currency,
                currency=rate.get('currency'),
                value_date=rate.get('date'),
                user=None,
                key=None
            )
            _rate.value = rate.get('value')
            _rate.save()
            output.append(_rate)
        return output

    def fetch_rates(self,
                    base_currency: str,
                    currency: str = None,
                    rate_service: str = None,
                    date_obj: date = date.today(),
                    to_obj: date = None) -> []:
        """
        Get rates from a service for a base currency and stores them in the database
        :param rate_service: Service class to fetch from
        :param currency: currency to obtain rate for
        :param base_currency: base currency to get rate from
        :param date_obj: date to fetch rates at
        :param to_obj: end of range
        :return: QuerySet of Rate
        """
        service_name = rate_service or settings.RATE_SERVICE
        try:
            rates = service(service_type='rates', service_name=service_name).fetch_rates(
                base_currency=base_currency,
                currency=currency,
                date_obj=date_obj,
                to_obj=to_obj)
            if not rates:
                return False
        except RatesNotAvailableError:
            return False
        return self.__sync_rates__(rates=rates, base_currency=base_currency)

    def rate_at_date(self,
                     currency: str,
                     key: str = None,
                     base_currency: str = settings.BASE_CURRENCY,
                     date_obj: date = date.today()) -> BaseRate:
        """
        Get a rate at a given date
        :param currency: target currency
        :param base_currency: destination currency
        :param key: User key
        :param date_obj: date at which to fetch the rate
        """
        rate = self.find_rate(
            currency=currency,
            key=key,
            base_currency=base_currency,
            date_obj=date_obj)
        if rate.pk:
            return rate
        return Rate()

    @classmethod
    def currency_shortest_path(cls, currency: str, base_currency: str, key: str = None,
                               date_obj: date = date.today()) -> [str]:
        """
        Return the shortest path between 2 currencies for the given date
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :return List of currency codes to go from currency to base currency
        """
        rates = Rate.objects.filter(value_date=date_obj).filter(
            models.Q(user=None) | models.Q(key=key))
        rates_couples = rates.values('currency', 'base_currency', 'value', 'key')
        graph = nx.Graph()
        for k in rates_couples:
            weight = 0.5 if k['base_currency'] == 'EUR' or k['currency'] == 'EUR' else 1
            weight *= (0.5 if k['key'] else 1)
            graph.add_edge(u_of_edge=k['currency'], v_of_edge=k['base_currency'], weight=weight)
        try:
            return nx.shortest_path(graph, currency, base_currency, weight='weight')
        except nx.exception.NetworkXNoPath as exc:
            raise NoRateFound(
                f"Rate {currency} to {base_currency} on "
                f"key {key} at date {date_obj} does not exist") \
                from exc

    def find_rate(self, currency: str,
                  rate_service: str = None,
                  key: str = None,
                  base_currency: str = settings.BASE_CURRENCY,
                  date_obj: date = date.today(),
                  use_forex: bool = False) -> BaseRate:
        """
        Find rate based on Floyd Warshall algorithm
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :param rate_service: Rate service to use
        :param use_forex: use rate service to fill the gaps
        """
        if use_forex:
            if not self.fetch_rates(
                    base_currency=base_currency,
                    currency=currency,
                    rate_service=rate_service,
                    date_obj=date_obj):
                return Rate()
        try:
            rates = self.currency_shortest_path(
                currency=currency,
                base_currency=base_currency,
                key=key,
                date_obj=date_obj
            )
        except NoRateFound:
            # No relation found, try fetching rate
            return self.find_rate(
                currency=currency,
                rate_service=rate_service,
                key=key,
                base_currency=base_currency,
                date_obj=date_obj,
                use_forex=True
            )
        # Direct connection between rates
        if len(rates) == 2:
            return Rate.objects.filter(
                currency=currency,
                base_currency=base_currency,
                value_date=date_obj
            ).filter(
                models.Q(key=key) | models.Q(user__isnull=True)
            ).order_by('-key').first()
        else:
            conv_value = 1
            for i in range(len(rates) - 1):
                from_cur, to_cur = rates[i:i + 2]
                rate = self.find_rate(
                        currency=from_cur,
                        base_currency=to_cur,
                        key=key,
                        date_obj=date_obj,
                        use_forex=False)
                if rate:
                    conv_value *= rate.value
                else:
                    raise NoRateFound(
                        f"rate {from_cur} -> {to_cur} for key {key} "
                        f"does not exist at date {date_obj}")
            rate = Rate.objects.create(
                key=key,
                value_date=date_obj,
                currency=currency,
                base_currency=base_currency,
                value=conv_value
            )
            return rate


class Rate(BaseRate):
    """
    Class Rate
    """
    user = models.ForeignKey(User, related_name='rates', on_delete=models.PROTECT, null=True)
    key = models.CharField("User defined categorization key",
                           max_length=255, default=None, db_index=True, null=True)
    value_date = models.DateField("Date of value")
    value = models.FloatField("Rate conversion factor", default=0)
    currency = models.CharField("Currency to convert from", max_length=3, db_index=True)
    base_currency = models.CharField("Currency to convert to", max_length=3, db_index=True,
                                     default='EUR')
    objects = RateManager()

    class Meta:
        """
        Meta
        """
        ordering = ['-value_date', ]
        indexes = [
            models.Index(fields=['base_currency', 'value_date']),
            models.Index(fields=['currency', 'value_date']),
            models.Index(fields=['currency', 'base_currency', 'value_date']),
            models.Index(fields=['key', 'currency', 'base_currency', 'value_date']),
        ]
        unique_together = [['key', 'currency', 'base_currency', 'value_date']]

    @classmethod
    def convert(cls, currency: str,
                user: User = None,
                key: str = None,
                base_currency: str = 'EUR',
                date_obj: date = date.today(),
                amount: float = 0) -> ConverterResult:
        """
        Convert rate
        :param user: Django User
        :param key: key for user
        :param base_currency: destination currency
        :param currency: source currency
        :param date_obj: date of the rate
        :param amount: amount to convert
        """
        converter = RateConverter(user=user, key=key, base_currency=base_currency)
        converter.add_data(
            {
                'currency': currency,
                'amount': amount,
                'date': date_obj
            }
        )
        result = converter.convert()
        return result


@receiver(post_save, sender=Rate)
def create_reverse_rate(sender, instance, created, **kwargs):
    """
    Create the rate object to revert rate when create a rate
    """
    if created and not Rate.objects.filter(
            user=instance.user,
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
    ).exists() and instance.value != 0:
        Rate.objects.create(
            user=instance.user,
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
            value=1 / instance.value
        )


class Amount:
    """
    Amount with a currency, a value and a date
    """
    currency = None
    amount = 0
    date_obj = None

    def __init__(self, currency: str, amount: float, date_obj: date):
        """
        Initialize amount
        """
        self.currency = currency
        self.amount = amount
        self.date_obj = date_obj

    def __repr__(self):
        """
        How do I look like
        """
        return f'{self.date_obj}: {self.currency} {self.amount}'


class RateConversionPayload:
    """
    Payload for conversion of amounts
    """
    data = None
    target = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, target, data=None, key=None, batch_id=None, eob=False):
        """
        Representation of the payload
        """
        self.data = data
        self.target = target
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class BulkRate:
    """
    Rate that is applied to a range of dates
    """
    base_currency = settings.BASE_CURRENCY
    currency = settings.BASE_CURRENCY
    value = 0
    key = None
    from_date = None
    to_date = None

    def __init__(self, base_currency, currency, value, key, from_date, to_date):
        """
        Initialize
        :param key: key for user
        :param base_currency: destination currency
        :param currency: source currency
        """
        self.base_currency = base_currency
        self.currency = currency
        self.value = value
        self.key = key
        self.from_date = from_date
        self.to_date = to_date

    def to_rates(self, user):
        """
        Create rates in the database
        """
        if not self.to_date:
            self.to_date = date.today()
        rates = []
        for i in range((self.to_date - self.from_date).days + 1):
            rate, created = Rate.objects.get_or_create(
                user=user,
                key=self.key,
                base_currency=self.base_currency,
                currency=self.currency,
                value_date=self.from_date + timedelta(i)
            )
            rate.value = self.value
            rate.save()
            rates.append(rate)
        return rates


class RateConverter(BaseConverter):
    """
    Converter of rates
    """
    base_currency = settings.BASE_CURRENCY
    cached_currencies = {}
    user = None
    key = None

    def __init__(self, user: User, id: str = None, key: str = None,
                 base_currency: str = settings.BASE_CURRENCY):
        """
        Initialize
        :param user: Django User
        :param key: key for user
        :param base_currency: destination currency
        """
        super(RateConverter, self).__init__(id=id)
        self.base_currency = base_currency
        self.user = user
        self.key = key

    def add_data(self, data: [Amount]) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super(RateConverter, self).add_data(data)
        self.cache_currencies()
        return errors

    def check_data(self, data: []) -> []:
        """
        Validates that the data contains
        - currency (str)
        - amount (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import RateAmountSerializer
        errors = []
        for line in data:
            serializer = RateAmountSerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    def cache_currencies(self):
        """
        Reads currencies in data and fetches rates, put them in memory
        """
        for line in self.data:
            self.cached_currencies[line.date_obj] = self.cached_currencies.get(line.date_obj) or {}
            rate = Rate.objects.rate_at_date(
                key=self.key,
                base_currency=self.base_currency,
                currency=line.currency,
                date_obj=line.date_obj)
            if rate.pk:
                self.cached_currencies[line.date_obj][line.currency] = rate.value

    def convert(self) -> ConverterResult:
        """
        Converts data to base currency
        """
        result = ConverterResult(id=self.id, target=self.base_currency)
        for amount in self.data:
            rate = self.cached_currencies[amount.date_obj][amount.currency]
            if rate:
                value = float(amount.amount) / rate
                result.increment_sum(value)
                detail = ConverterResultDetail(
                    unit=amount.currency,
                    original_value=amount.amount,
                    date=amount.date_obj,
                    conversion_rate=rate,
                    converted_value=value
                )
                result.detail.append(detail)
            else:
                error = ConverterResultError(
                    unit=amount.currency,
                    original_value=amount.amount,
                    date=amount.date_obj,
                    error=_('Rate could not be found')
                )
                result.errors.append(error)
        self.end_batch(result.end_batch())
        return result
