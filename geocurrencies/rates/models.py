from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import QuerySet
from django.dispatch import receiver

from geocurrencies.helpers import service
from .settings import *
from django.conf import settings

try:
    RATE_SERVICE = settings.RATE_SERVICE
except AttributeError:
    pass

from .services import RatesNotAvailableError, RateService


class RateManager(models.Manager):

    def __sync_rates__(self, rates: [], base_currency: str, date_obj: date, to_obj: date = None):
        """
        rates: array of dict of rates from service
        """
        output = []
        for rate in rates:
            _rate = Rate.objects.get_or_create(
                base_currency=base_currency,
                currency=rate.get('currency'),
                value_date=rate.get('date')
            )
            _rate.value = rate.get('value')
            _rate.save()
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
            rates = service(service_name).fetch_rates(
                base_cur=base_currency,
                currency=currency,
                date_obj=date_obj,
                to_obj=to_obj)
            if not rates:
                return False
        except RatesNotAvailableError:
            return False
        return self.__sync_rates__(base_currency=base_currency, date_obj=date_obj, to_obj=to_obj)

    def rate_at_date(self, currency, key=None, base_currency='EUR', date_obj=date.today()):
        # See here for process
        # https://app.lucidchart.com/documents/edit/cee5a97f-021f-4eab-8cf3-d66c88cf46f2/0_0?beaconFlowId=4B33C87C22AD8D63
        if rate := self.find_direct_rate(currency=currency, key=key, base_currency=base_currency, date_obj=date_obj):
            return rate
        if rate := self.find_pivot_rate(currency=currency, key=key, base_currency=base_currency, date_obj=date_obj):
            return rate
        return None

    def find_direct_rate(self, currency, key=None, base_currency='EUR', date_obj=date.today(), use_forex=False):
        rates = Rate.objects.filter(
            key=key,
            currency=currency,
            base_currency=base_currency,
            value_date=date_obj
        )
        if rates:
            return rates.latest('value_date')
        elif use_forex:
            c = CurrencyRates()
            c.get_rate(dest_cur=currency, base_cur=base_currency, date_obj=date_obj)
        return None

    def find_pivot_rate(self, currency, key=None, base_currency='EUR', date_obj=date.today()):
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
        ordering = ['-value_date',]
        indexes = [
            models.Index(fields=['currency', 'base_currency', 'value_date']),
            models.Index(fields=['key', 'currency', 'base_currency', 'value_date']),
        ]
        unique_together = [['key', 'currency', 'base_currency', 'value_date']]

    @classmethod
    def convert(cls, currency, key=None, base_currency='EUR', date_obj=date.today(), amount=0):
        rate = Rate.objects.rate_at_date(currency, key, base_currency, date_obj)
        return {
            'currency': rate.currency,
            'base': rate.base_currency,
            'date': date_obj,
            'exchange_rate': rate.value,
            'amount': amount,
            'converted_amount': rate.value * amount
        }


@receiver(post_save, sender=Rate)
def create_reverse_rate(sender, instance, created, **kwargs):
    if created and not Rate.objects.filter(
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
    ).exists() and instance.value != 0:
        Rate.objects.create(
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
            value=1 / instance.value
        )
