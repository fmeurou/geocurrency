import logging
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from geocurrency.converters.models import BaseConverter, ConverterResult, ConverterResultDetail, ConverterResultError
from geocurrency.core.helpers import service

try:
    RATE_SERVICE = settings.RATE_SERVICE
except AttributeError:
    pass

from .services import RatesNotAvailableError


class BaseRate(models.Model):
    value = None

    class Meta:
        abstract = True


class RateManager(models.Manager):

    def __sync_rates__(self, rates: [], base_currency: str, date_obj: date, to_obj: date = None):
        """
        rates: array of dict of rates from service
        """
        output = []
        for rate in rates:
            _rate, created = Rate.objects.get_or_create(
                base_currency=base_currency,
                currency=rate.get('currency'),
                value_date=rate.get('date')
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
        return self.__sync_rates__(rates=rates, base_currency=base_currency, date_obj=date_obj, to_obj=to_obj)

    def rate_at_date(self,
                     currency: str,
                     key: str = None,
                     base_currency: str = settings.BASE_CURRENCY,
                     date_obj: date = date.today()) -> BaseRate:
        # See here for process
        # https://app.lucidchart.com/documents/edit/cee5a97f-021f-4eab-8cf3-d66c88cf46f2/0_0?beaconFlowId=4B33C87C22AD8D63
        rate = self.find_direct_rate(
                currency=currency,
                key=key,
                base_currency=base_currency,
                date_obj=date_obj)
        if rate.pk:
            return rate
        rate = self.find_pivot_rate(currency=currency, key=key, base_currency=base_currency, date_obj=date_obj)
        if rate.pk:
            return rate
        return Rate()

    def find_direct_rate(self,
                         currency: str,
                         rate_service: str = None,
                         key: str = None,
                         base_currency: str = settings.BASE_CURRENCY,
                         date_obj: date = date.today(),
                         use_forex: bool = False) -> BaseRate:
        """
        Find base_currency / currency at date with the specific key
        """
        rates = Rate.objects.filter(
            key=key,
            currency=currency,
            base_currency=base_currency,
            value_date=date_obj
        )
        if rates:
            return rates.latest('value_date')
        elif use_forex:
            try:
                rates = self.fetch_rates(
                    rate_service=rate_service,
                    base_currency=base_currency,
                    currency=currency,
                    date_obj=date_obj)
                if not rates:
                    return Rate()
                return Rate.objects.get(
                    key=key,
                    currency=currency,
                    base_currency=base_currency,
                    value_date=date_obj
                )
            except RatesNotAvailableError as e:
                logging.error(e)
                return Rate()
        return Rate()

    def find_pivot_rate(self,
                        currency: str,
                        key: str = None,
                        base_currency: str = 'EUR',
                        date_obj: date = date.today()):
        # We simplify the algorithm to only one pivot
        # Most currencies convert to Euro or Dollar
        # So there is an obvious path in finding only one pivot

        rates = Rate.objects.filter(
            key=key,
            currency=currency,
            value_date__lte=date_obj
        )
        pivot_rates = Rate.objects.filter(
            key=key,
            currency__in=rates.values_list('base_currency', flat=True),
            base_currency=base_currency,
            value_date=date_obj
        )
        if not rates:
            # Can‘t find any rate for this client for this date, using standard rates
            return self.find_direct_rate(
                currency=currency,
                base_currency=base_currency,
                date_obj=date_obj,
                use_forex=True)
        if pivot_rates.exists():
            pivot_rate = pivot_rates.latest('value_date')
            rate = rates.filter(base_currency=pivot_rate.currency).latest('value_date')
            # It exists! let‘s store it
            rate = Rate.objects.create(
                key=key,
                value_date=date_obj,
                currency=rate.currency,
                base_currency=base_currency,
                value=rate.value * pivot_rate.value
            )
            return rate
        else:
            rate = rates.latest('value_date')
            pivot_rate = self.find_direct_rate(
                currency=rate.base_currency,
                base_currency=base_currency,
                date_obj=date_obj,
                use_forex=True
            )
            if pivot_rate:
                # It exists! let‘s store it
                rate = Rate.objects.create(
                    key=key,
                    value_date=date_obj,
                    currency=rate.currency,
                    base_currency=base_currency,
                    value=rate.value * pivot_rate.value
                )
                return rate
        return None


class Rate(BaseRate):
    user = models.ForeignKey(User, related_name='rates', on_delete=models.PROTECT, null=True)
    key = models.CharField(max_length=255, default=None, db_index=True, null=True)
    value_date = models.DateField()
    value = models.FloatField(default=0)
    currency = models.CharField(max_length=3)
    base_currency = models.CharField(max_length=3, default='EUR')
    objects = RateManager()

    class Meta:
        ordering = ['-value_date', ]
        indexes = [
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
    currency = None
    amount = 0
    date_obj = None

    def __init__(self, currency: str, amount: float, date_obj: date):
        self.currency = currency
        self.amount = amount
        self.date_obj = date_obj

    def __repr__(self):
        return f'{self.date_obj}: {self.currency} {self.amount}'


class RateConversionPayload:
    data = None
    target = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, target, data=None, key=None, batch_id=None, eob=False):
        self.data = data
        self.target = target
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class BulkRate:
    base_currency = settings.BASE_CURRENCY
    currency = settings.BASE_CURRENCY
    value = 0
    key = None
    from_date = None
    to_date = None

    def __init__(self, base_currency, currency, value, key, from_date, to_date):
        self.base_currency = base_currency
        self.currency = currency
        self.value = value
        self.key = key
        self.from_date = from_date
        self.to_date = to_date

    def to_rates(self, user):
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
    base_currency = settings.BASE_CURRENCY
    cached_currencies = {}
    user = None
    key = None

    def __init__(self, user: User, id: str = None, key: str = None, base_currency: str = settings.BASE_CURRENCY):
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
