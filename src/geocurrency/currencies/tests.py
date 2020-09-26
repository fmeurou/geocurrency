from datetime import date
from django.test import TestCase
from iso4217 import Currency as Iso4217
from rest_framework import status
from rest_framework.test import APIClient

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
        self.assertEqual(c.symbol, '€')

    def test_is_valid(self):
        self.assertTrue(Currency.is_valid('EUR'))
        self.assertFalse(Currency.is_valid('REU'))

    def test_get_for_country(self):
        currencies = Currency.get_for_country('FR')
        self.assertIsNotNone(currencies)
        c = currencies[0]
        self.assertEqual(c.name, 'eur')
        self.assertEqual(c.value, 'EUR')
        self.assertEqual(c.currency_name, 'Euro')
        self.assertEqual(c.number, 978)
        self.assertEqual(c.code, 'EUR')

    def test_countries(self):
        c = Currency('EUR')
        self.assertIsNotNone(c.countries)

    def test_get_rates(self):
        c = Currency('EUR')
        rates = c.get_rates()
        self.assertIsNotNone(rates)

    def test_list_request(self):
        client = APIClient()
        response = client.get('/currencies/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Currency.all_currencies()))
        self.assertEqual(response.data[0].get('code'), 'AFN')

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get('/currencies/EUR/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), 'EUR')
        self.assertEqual(response.data.get('symbol'), '€')

    def test_get_countries_request(self):
        client = APIClient()
        response = client.get('/currencies/AFN/countries/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('alpha_2'), 'AF')

    def test_get_rates_request(self):
        client = APIClient()
        response = client.get('/currencies/AFN/rates/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_base_request(self):
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'base_currency': 'USD'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_start_date_request(self):
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'start_date': date.today().strftime('%Y-%m-%d')
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_end_date_request(self):
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'end_date': date.today().strftime('%Y-%m-%d')
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
