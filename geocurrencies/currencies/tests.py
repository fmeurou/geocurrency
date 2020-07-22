from iso4217 import Currency as Iso4217
from datetime import date
from django.test import TestCase
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

    def test_get_for_country(self):
        c = Currency.get_for_country('FR')
        self.assertEqual(c.name, 'eur')
        self.assertEqual(c.value, 'EUR')
        self.assertEqual(c.currency_name, 'Euro')
        self.assertEqual(c.number, 978)
        self.assertEqual(c.code, 'EUR')

    def test_convert(self):
        c = Currency('EUR')

    def test_list_request(self):
        client = APIClient()
        response = client.get('/currencies/', format='json')
        first_country = Currency.all_currencies()[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Currency.all_currencies()))
        self.assertEqual(response.data[0].get('code'), 'AFN')

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get('/currencies/EUR/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), 'EUR')

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