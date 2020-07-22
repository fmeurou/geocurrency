from datetime import date
from django.test import TestCase
from .models import Rate


class RateTestCase(TestCase):
    base_currency = 'EUR'
    currency = 'USD'

    def test_fetch_rates(self):
        rates = Rate.objects.fetch_rates(base_cur=self.base_currency)
        self.assertIsNotNone(rates)

    def test_fetch_rates_with_date(self):
        rates = Rate.objects.fetch_rates(base_cur=self.base_currency, date_obj=date(year=2020, month=6, day=1))
        self.assertIsNotNone(rates)

    def test_fetch_rate(self):
        rate = Rate.objects.fetch_rate(base_cur=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate)

    def test_fetch_rate_with_date(self):
        rate = Rate.objects.fetch_forex_rate(
            base_cur=self.base_currency, currency=self.currency,
            date_obj=date(year=2020, month=6, day=1)
        )
        self.assertIsNotNone(rate)

    def test_find_direct_rate(self):
        Rate.objects.fetch_rate(base_cur=self.base_currency, currency=self.currency)
        rate = Rate.objects.find_direct_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate, msg="no direct rate found")

    def test_find_pivot_rate(self):
        Rate.objects.fetch_rate(base_cur=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rate(base_cur=self.currency, currency='JPY')
        rate = Rate.objects.find_pivot_rate(base_currency=self.base_currency, currency='JPY')
        self.assertIsNotNone(rate, msg="no pivot rate found")

    def test_rate_at_date(self):
        Rate.objects.fetch_rate(base_cur=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rate(base_cur=self.currency, currency='JPY')
        rate = Rate.objects.find_direct_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate, msg="no direct rate found")
        rate = Rate.objects.find_pivot_rate(base_currency=self.base_currency, currency='JPY')
        self.assertIsNotNone(rate, msg="no pivot rate found")
