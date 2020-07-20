from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from forex_python.converter import CurrencyRates


class RateManager(models.Manager):

    @classmethod
    def fetch_forex_rates(self, base_cur, date_obj=None):
        """
        Get rates for a base currency and stores them in the database
        """
        c = CurrencyRates()
        rates = c.get_rates(base_cur=base_cur, date_obj=date.today())
        if not rates:
            return False
        existing_rates = Rate.objects.filter(base_currency=base_cur, start_date=date_obj, end_date=date_obj)
        for existing_rate in existing_rates:
            existing_rate.value = rates[existing_rate.currency].value
            existing_rate.save()
        for currency in set(rates.keys()) - set(existing_rates.values_list('currency', flat=True)):
            Rate.objects.create(
                key=None,
                start_date=date_obj,
                end_date=date_obj,
                currency=currency,
                base_currency=base_cur,
                value=rates[currency]
            )
        return Rate.objects.filter(base_currency=base_cur, start_date=date_obj, end_date=date_obj)

    def fetch_forex_rate(self, dest_cur, base_cur, date_obj=date.today()):
        """
        Get rate between a base currency and a currency and stores it in the database
        """
        c = CurrencyRates()
        value = c.get_rate(dest_cur=dest_cur, base_cur=base_cur, date_obj=date_obj)
        try:
            # Do we have the rate in database ? update it
            rate = Rate.objects.get(
                key=None,
                start_date=date_obj,
                end_date=date_obj,
                currency=dest_cur,
                base_currency=base_cur
            )
            rate.save()
        except Rate.DoesNotExist:
            # We don‘t have the rate ? create it
            rate = Rate.objects.create(
                key=None,
                start_date=date_obj,
                end_date=date_obj,
                currency=dest_cur,
                base_currency=base_cur,
                value=value
            )
        return rate

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
            start_date__lte=date_obj,
            end_date__gte=date_obj
        )
        if rates:
            return rates.latest('start_date')
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
            start_date__lte=date_obj,
            end_date__gte=date_obj
        )
        pivot_rates = Rate.objects.filter(
            key=key,
            currency__in=rates.values_list('base_currency', flat=True),
            base_currency=base_currency,
            start_date__lte=date_obj,
            end_date__gte=date_obj
        )
        if not rates:
            # Can‘t find any rate for this client for this date, using standard rates
            return self.find_direct_rate(
                currency=currency,
                base_currency=base_currency,
                date_obj=date_obj,
                use_forex=True)
        if pivot_rates.exists():
            pivot_rate = pivot_rates.latest('start_date')
            rate = rates.filter(base_currency=pivot_rate.currency).latest('start_date')
            # It exists! let‘s store it
            rate = Rate.objects.create(
                key=key,
                start_date=date_obj,
                end_date=date_obj,
                currency=rate.currency,
                base_currency=base_currency,
                value=rate.value * pivot_rate.value
            )
            return rate
        else:
            rate = rates.latest('start_date')
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
                    start_date=date_obj,
                    end_date=date_obj,
                    currency=rate.currency,
                    base_currency=base_currency,
                    value=rate.value * pivot_rate.value
                )
                return rate
        return None


class Rate(models.Model):
    user = models.ForeignKey(User, related_name='rates', on_delete=models.PROTECT, null=True)
    key = models.CharField(max_length=255, default=None, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.FloatField(default=0)
    currency = models.CharField(max_length=3)
    base_currency = models.CharField(max_length=3, default='EUR')

    class Meta:
        ordering = ['-start_date', '-end_date']
        indexes = [
            models.Index(fields=['currency', 'base_currency', 'start_date', 'end_date']),
            models.Index(fields=['key', 'currency', 'base_currency', 'start_date', 'end_date']),
        ]
        unique_together = [['key', 'currency', 'base_currency', 'start_date', 'end_date']]

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
            start_date=instance.start_date,
            end_date=instance.end_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
    ).exists() and instance.value != 0:
        Rate.objects.create(
            key=instance.key,
            start_date=instance.start_date,
            end_date=instance.end_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
        ).update(value=1 / instance.value)
