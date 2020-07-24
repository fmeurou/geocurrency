import logging
import pickle
import uuid
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from geocurrencies.helpers import service
from .settings import *

try:
    RATE_SERVICE = settings.RATE_SERVICE
except AttributeError:
    pass

from .services import RatesNotAvailableError


class Rate:
    pass


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
                     date_obj: date = date.today()) -> Rate:
        # See here for process
        # https://app.lucidchart.com/documents/edit/cee5a97f-021f-4eab-8cf3-d66c88cf46f2/0_0?beaconFlowId=4B33C87C22AD8D63
        if rate := self.find_direct_rate(currency=currency, key=key, base_currency=base_currency, date_obj=date_obj):
            return rate
        if rate := self.find_pivot_rate(currency=currency, key=key, base_currency=base_currency, date_obj=date_obj):
            return rate
        return None

    def find_direct_rate(self,
                         currency: str,
                         rate_service: str = None,
                         key: str = None,
                         base_currency: str = settings.BASE_CURRENCY,
                         date_obj: date = date.today(),
                         use_forex: bool = False) -> Rate:
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
                    base_currency=base_currency,
                    currency=currency,
                    date_obj=date_obj)
                if not rates:
                    return None
                return Rate.objects.get(
                    key=key,
                    currency=currency,
                    base_currency=base_currency,
                    value_date=date_obj
                )
            except RatesNotAvailableError as e:
                logging.error(e)
                return None
        return None

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


class Rate(models.Model):
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
    def convert(self, currency, key=None, base_currency='EUR', date_obj=date.today(), amount=0):
        converter = Converter(self.user, key=key, base_currency=base_currency)
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


class Batch:
    id = None
    status = None

    def __init__(self, id, status):
        self.id = id
        self.status = status


class Amount:
    currency = None
    amount = 0
    date_obj = None

    def __init__(self, currency, amount, date_obj):
        self.currency = currency
        self.amount = amount
        self.date_obj = date_obj

    def __repr__(self):
        return f'{self.date_obj}: {self.currency} {self.amount}'


class Converter:
    pass


class Converter:
    INITIATED_STATUS = 'initiated'
    INSERTING_STATUS = 'inserting'
    PENDING_STATUS = 'pending'
    FINISHED = 'finished'
    id = None
    user = None
    base_currency = settings.BASE_CURRENCY
    status = INITIATED_STATUS
    data = []
    converted_lines = []
    aggregated_result = {}
    cached_currencies = {}

    def __init__(self, user: User, id: str = None, key: str = None, base_currency: str = settings.BASE_CURRENCY):
        self.base_currency = base_currency
        self.user = user
        self.key = key
        self.id = id or uuid.uuid4()
        self.data = []

    @classmethod
    def load(cls, id: str) -> Converter:
        obj = cache.get(id)
        if obj:
            return pickle.loads(obj)
        raise KeyError(f"Conversion with id {id} not found in cache")

    def save(self):
        cache.set(self.id, pickle.dumps(self))

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        if errors := self.check_data(data):
            return errors
        self.status = self.INSERTING_STATUS
        self.cache_currencies()
        self.save()
        return []

    def end_batch(self):
        self.status = self.PENDING_STATUS

    def check_data(self, data):
        """
        Validates that the data contains
        - currency (str)
        - amount (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import AmountSerializer
        errors = []
        for line in data:
            serializer = AmountSerializer(data=line)
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
            if rate:
                self.cached_currencies[line.date_obj][line.currency] = rate.value

    def convert(self) -> dict:
        """
        Converts data to base currency
        """
        output = {
            'id': self.id,
            'target': self.base_currency,
            'detail': [],
            'sum': 0,
            'status': None,
            'errors': []
        }
        sum = 0
        for amount in self.data:
            rate = self.cached_currencies[amount.date_obj][amount.currency]
            if rate:
                value = float(amount.amount) / rate
                sum += value
                output['detail'].append({
                    'currency': amount.currency,
                    'original_amount': amount.amount,
                    'date': amount.date_obj,
                    'rate': rate,
                    'converted_amount': value
                })
            else:
                output['errors'].append({
                    'currency': amount.currency,
                    'original_amount': amount.amount,
                    'date': amount.date_obj
                })
        output['sum'] = sum
        output['status'] = self.FINISHED
        self.status = self.FINISHED
        return output
