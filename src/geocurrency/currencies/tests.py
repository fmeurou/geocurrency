"""
Currencies tests
"""

from datetime import date
from django.test import TestCase
from iso4217 import Currency as Iso4217
from rest_framework import status
from rest_framework.test import APIClient

from .models import Currency


class CurrencyTestCase(TestCase):
    """
    Tests for Currency class
    """

    def test_all_currencies(self):
        """
        Test listing of all currencies
        """
        self.assertEqual(len(list(Currency.all_currencies())), len(Iso4217))

    def test_ordered_all_currencies(self):
        """
        Test sorting of list of currencies
        """
        self.assertEqual(
            list(Currency.all_currencies(ordering='code'))[0].code, 'AED')
        self.assertEqual(
            list(Currency.all_currencies(ordering='name'))[0].code, 'AED')
        self.assertEqual(
            list(Currency.all_currencies(ordering='currency_name'))[0].code,
            'AFN')
        self.assertEqual(
            list(Currency.all_currencies(ordering='exponent'))[0].code, 'XOF')
        self.assertEqual(
            list(Currency.all_currencies(ordering='number'))[0].code, 'ALL')
        self.assertEqual(
            list(Currency.all_currencies(ordering='value'))[0].code, 'AED')

    def test_creation(self):
        """
        Test creation of a currency
        """
        c = Currency('EUR')
        self.assertEqual(c.name, 'eur')
        self.assertEqual(c.value, 'EUR')
        self.assertEqual(c.currency_name, 'Euro')
        self.assertEqual(c.number, 978)
        self.assertEqual(c.code, 'EUR')
        self.assertEqual(c.symbol, '€')

    def test_is_valid(self):
        """
         Test currency validation
        """
        self.assertTrue(Currency.is_valid('EUR'))
        self.assertFalse(Currency.is_valid('REU'))

    def test_get_for_country(self):
        """
        Test getting currency for a country
        """
        currencies = Currency.get_for_country('FR')
        self.assertIsNotNone(currencies)
        c = list(currencies)[0]
        self.assertEqual(c.name, 'eur')
        self.assertEqual(c.value, 'EUR')
        self.assertEqual(c.currency_name, 'Euro')
        self.assertEqual(c.number, 978)
        self.assertEqual(c.code, 'EUR')

    def test_countries(self):
        """
        Test list of countrries for a currency
        """
        c = Currency('EUR')
        self.assertIsNotNone(c.countries)

    def test_get_rates(self):
        """
        Test getting rates for a currency
        """
        c = Currency('EUR')
        rates = c.get_rates()
        self.assertIsNotNone(rates)


class CurrencyAPITestCase(TestCase):
    """
    Tests for Currency API
    """

    def test_list_request(self):
        """
        Test list of currencies
        """
        client = APIClient()
        response = client.get('/currencies/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Currency.all_currencies()))
        self.assertEqual(response.data[0].get('code'), 'AED')

    def test_list_ordered_request(self):
        """
        Test list with sorting
        """
        client = APIClient()
        response = client.get('/currencies/',
                              data={'ordering': 'code'},
                              format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Currency.all_currencies()))
        self.assertEqual(response.data[0].get('code'), 'AED')

    def test_retrieve_request(self):
        """
        Test retrieval of a currency
        """
        client = APIClient()
        response = client.get('/currencies/EUR/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), 'EUR')
        self.assertEqual(response.data.get('symbol'), '€')

    def test_get_countries_request(self):
        """
        Test listing countries for a currency
        """
        client = APIClient()
        response = client.get('/currencies/AFN/countries/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('alpha_2'), 'AF')

    def test_get_rates_request(self):
        """
        Test listing rates for a currency (use /rates/ instead)
        """
        client = APIClient()
        response = client.get('/currencies/AFN/rates/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_base_request(self):
        """
        Test listing rates for a base currency (use /rates/ instead)
        """
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'base_currency': 'USD'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_start_date_request(self):
        """
        Test listing rates for a currency (use /rates/ instead) from a date
        """
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'start_date': date.today().strftime('%Y-%m-%d')
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rates_with_end_date_request(self):
        """
        Test listing rates for a currency (use /rates/ instead) with end date
        """
        client = APIClient()
        response = client.get(
            '/currencies/AFN/rates/',
            data={
                'end_date': date.today().strftime('%Y-%m-%d')
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
