from iso4217 import Currency as Iso4217
from django.test import TestCase

from .models import Currency


class CurrencyTestCase(TestCase):

    def test_all_currencies(self):
        self.assertEqual(len(Currency.all_currencies()), len(Iso4217))

    def test_creation(self):
        c = Currency('EUR')
        self.assertEqual(c.name, 'eur')
        self.assertEqual(c.value, 'EUR')
        self.assertEqual(c.currency_name, 'Euro')
        self.assertEqual(c.number, 978)
        self.assertEqual(c.code, 'EUR')

