"""
Rates module tests
"""
import datetime
import uuid
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Rate, RateConverter, NoRateFound
from .serializers import RateAmountSerializer


class RateTest(TestCase):
    """
    Rate object tests
    """
    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
        """
        Setup test environment
        """
        settings.RATE_SERVICE = 'forex'
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()
        self.amounts = [
            {
                'currency': 'USD',
                'amount': 100,
                'date_obj': '2020-07-22'
            },
            {
                'currency': 'AUD',
                'amount': 50,
                'date_obj': '2020-07-23'
            },
        ]
        self.trash_amounts = [
            {
                'currency': 'USD',
                'amount': 'toto',
                'date_obj': '01/01/2020'
            },
            {
                'currency': 'LOL',
                'date_obj': '2020-07-23'
            },
            {
                'date_obj': '2020-07-23'
            },
            {
                'currency': 'JPY',
            },
        ]

    def test_fetch_rates(self):
        """
        Test fetching of rates from service
        """
        rates = Rate.objects.fetch_rates(base_currency=self.base_currency)
        self.assertIsNotNone(rates)

    def test_fetch_rates_with_date(self):
        """
        Test fetching of rates at a given date
        """
        rates = Rate.objects.fetch_rates(base_currency=self.base_currency,
                                         date_obj=date(year=2020, month=6, day=1))
        self.assertIsNotNone(rates)

    def test_fetch_rate(self):
        """
        Test fectch of a specific conversion rate
        """
        rate = Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate)

    def test_fetch_rate_with_date(self):
        """
        Test of specific conversion rate at a given date
        """
        rate = Rate.objects.fetch_rates(
            base_currency=self.base_currency, currency=self.currency,
            date_obj=date(year=2020, month=6, day=1)
        )
        self.assertIsNotNone(rate)

    def test_find_rate(self):
        """
        Find a rate between currencies
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        rate = Rate.objects.find_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate, msg="no rate found")

    def test_find_pivot_rate(self):
        """
        Find rate between currencies that are not directly linked
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        rate = Rate.objects.find_rate(base_currency=self.base_currency, currency='AUD')
        self.assertIsNotNone(rate, msg="no rate found")

    def test_rate_at_date(self):
        """
        Find rate at a specific date
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        rate = Rate.objects.find_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate.pk, msg="no direct rate found")
        rate = Rate.objects.find_rate(base_currency=self.base_currency, currency='AUD')
        self.assertIsNotNone(rate.pk, msg="no pivot rate found")

    def test_custom_rate(self):
        """
        Create a custom rate
        """
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AUD',
            base_currency='AFN',
            value=0.123,
            value_date='2021-01-01'
        )
        self.assertIsNotNone(
            Rate.objects.filter(user=self.user, key=self.key, base_currency='AFN', currency='AUD'))

    def test_find_rate_chain(self):
        """
        Test find rate with keys
        """
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AUD',
            base_currency='AFN',
            value=0.123,
            value_date='2021-01-01'
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='JPY',
            value=200,
            value_date='2021-01-01'
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='JPY',
            base_currency='BND',
            value=13,
            value_date='2021-01-01'
        )
        rates = Rate.objects.currency_shortest_path(
            currency='AUD', base_currency='BND', key=self.key, date_obj='2021-01-01')
        self.assertEqual(rates, ['AUD', 'AFN', 'JPY', 'BND'])

    def test_find_mixed_rate_chain(self):
        """
        Test find rate with keys with gaps in the key chain
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency)
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='ARS',
            base_currency='AFN',
            value=0.123,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='BND',
            value=200,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='BND',
            base_currency='JPY',
            value=13,
            value_date=datetime.date.today()
        )
        rates = Rate.objects.currency_shortest_path(
            currency='ARS', base_currency='EUR', key=self.key, date_obj=datetime.date.today())
        self.assertEqual(rates, ['ARS', 'AFN', 'BND', 'JPY', 'EUR'])

    def test_no_rate_path(self):
        """
        Test what happens if no rate is found
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency)
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='ARS',
            base_currency='AFN',
            value=0.123,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='BND',
            value=200,
            value_date=datetime.date.today()
        )
        self.assertRaises(
            NoRateFound,
            Rate.objects.currency_shortest_path,
            currency='ARS',
            base_currency='EUR',
            key=self.key,
            date_obj=datetime.date.today()
        )

    def test_find_rate_custom(self):
        """
        Test conversion between rates with custom rate
        """
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='ARS',
            base_currency='AFN',
            value=0.123,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='BND',
            value=200,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='BND',
            base_currency='JPY',
            value=13,
            value_date=datetime.date.today()
        )
        rate = Rate.objects.find_rate(
            base_currency='JPY',
            currency='ARS',
            date_obj=datetime.date.today(),
            key=self.key)
        self.assertEqual(rate.value, 0.123 * 200 * 13)

    def test_find_rate_mixed(self):
        """
        Test conversion between rates with custom and standard rates
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency)
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='ARS',
            base_currency='AFN',
            value=0.123,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='BND',
            value=200,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='BND',
            base_currency='JPY',
            value=13,
            value_date=datetime.date.today()
        )
        jpy_eur = Rate.objects.get(
            base_currency='EUR',
            currency='JPY',
            value_date=datetime.date.today()
        )
        rate = Rate.objects.find_rate(
            base_currency='EUR',
            currency='ARS',
            date_obj=datetime.date.today(),
            key=self.key)
        self.assertEqual(rate.value, 0.123 * 200 * 13 * jpy_eur.value)

    def test_find_rate_override(self):
        """
        Test having 2 rates for the same period, with a custom and a standard one
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency)
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='ARS',
            base_currency='AFN',
            value=0.123,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='AFN',
            base_currency='BND',
            value=200,
            value_date=datetime.date.today()
        )
        Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='BND',
            base_currency='JPY',
            value=13,
            value_date=datetime.date.today()
        )
        jpy_eur_custom = Rate.objects.create(
            user=self.user,
            key=self.key,
            currency='JPY',
            base_currency='EUR',
            value=100,
            value_date=datetime.date.today()
        )
        jpy_eur = Rate.objects.get(
            base_currency='EUR',
            currency='JPY',
            user__isnull=True,
            value_date=datetime.date.today()
        )
        rate = Rate.objects.find_rate(
            base_currency='EUR',
            currency='ARS',
            date_obj=datetime.date.today(),
            key=self.key)
        self.assertEqual(rate.value, 0.123 * 200 * 13 * jpy_eur_custom.value)


class RateAPITest(TestCase):
    """
    Rate object tests
    """
    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
        """
        Setup test environment
        """
        settings.RATE_SERVICE = 'forex'
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()
        self.amounts = [
            {
                'currency': 'USD',
                'amount': 100,
                'date_obj': '2020-07-22'
            },
            {
                'currency': 'AUD',
                'amount': 50,
                'date_obj': '2020-07-23'
            },
        ]
        self.trash_amounts = [
            {
                'currency': 'USD',
                'amount': 'toto',
                'date_obj': '01/01/2020'
            },
            {
                'currency': 'LOL',
                'date_obj': '2020-07-23'
            },
            {
                'date_obj': '2020-07-23'
            },
            {
                'currency': 'JPY',
            },
        ]

    def test_post_rate(self):
        """
        Test rate creation
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(response.status_code, 201)
        response = client.get(
            '/rates/',
            format='json')
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 2)
        else:
            self.assertEqual(len(response.json()), 2)

    def test_post_rate_without_key(self):
        """
        Test standard rate creation without key
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(
            '/rates/',
            data={
                'key': '',
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_request(self):
        """
        Test rate list
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        client = APIClient()
        response = client.get(
            '/rates/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stats_request(self):
        """
        Test rate stats
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        client = APIClient()
        response = client.get(
            '/rates/stats/',
            data={},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_connected_list_request(self):
        """
        Test rates list for authenticated user
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', post_response.json())
        response = client.get(
            '/rates/',
            format='json')
        anon_client = APIClient()
        anon_response = anon_client.get(
            '/rates/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(anon_response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']),
                             len(anon_response.json()['results']) + 2)
        else:
            self.assertEqual(len(response.json()), len(anon_response.json()) + 2)

    def test_list_with_key_request(self):
        """
        Test list with key argument
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            '/rates/',
            data={'key': self.key},
            format='json')
        if 'results' in response.json():
            self.assertEqual(response.json()['results'][0]['key'], str(self.key))
        else:
            self.assertEqual(response.json()[0]['key'], str(self.key))

    def test_list_with_key_or_null_request(self):
        """
        Test key_or_null filter
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        response = client.get(
            '/rates/',
            data={'key_or_null': self.key},
            format='json')
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 3)
        else:
            self.assertEqual(len(response.json()), 3)

    def test_list_with_key_isnull_request(self):
        """
        Test key_isnull filter
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        response = client.get(
            '/rates/',
            data={'key_isnull': self.key},
            format='json')
        if 'results' in response.json():
            self.assertEqual(response.json()['results'][0]['key'], None)
        else:
            self.assertEqual(response.json()[0]['key'], None)

    def test_list_with_key_and_currency_request(self):
        """
        Test key and currency filters
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            '/rates/',
            data={'key': self.key, 'currency': 'USD'},
            format='json')
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 1)
        else:
            self.assertEqual(len(response.json()), 1)

    def test_stats_with_key_and_currency_request(self):
        """
        Test stats with key and currency filters
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-02',
                'value': 1.20,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            '/rates/stats/',
            data={'key': self.key, 'currency': 'EUR'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_with_key_and_base_currency_request(self):
        """
        Test stats with key and base_currency filters
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'value_date': '2020-01-01',
                'value': 1.10,
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            '/rates/',
            data={'key': self.key, 'base_currency': 'USD'},
            format='json')
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 1)
        else:
            self.assertEqual(len(response.json()), 1)

    def test_retrieve_request(self):
        """
        Test retreiving a specific rate
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        rate = Rate.objects.first()
        client = APIClient()
        response = client.get(
            f'/rates/{rate.pk}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], rate.pk)

    def test_bulk_create_request(self):
        """
        Test of bulk creation
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/bulk/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'from_date': '2020-01-01',
                'to_date': '2020-09-01',
                'value': 1.10
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(post_response.json()),
                         (datetime.date(year=2020, month=9, day=1) - datetime.date(year=2020,
                                                                                   month=1,
                                                                                   day=1)).days + 1)

    def test_latest_currency_request(self):
        """
        Test filtering latest values for currency
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/rates/bulk/',
            data={
                'key': self.key,
                'currency': 'USD',
                'base_currency': 'EUR',
                'from_date': '2020-01-01',
                'to_date': '2020-09-01',
                'value': 1.10
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            '/rates/?currency_latest_values=USD'
        )
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 1)
        else:
            self.assertEqual(len(response.json()), 1)
        response = client.get(
            '/rates/?base_currency_latest_values=EUR'
        )
        if 'results' in response.json():
            self.assertEqual(len(response.json()['results']), 1)
        else:
            self.assertEqual(len(response.json()), 1)


class RateConverterTest(TestCase):
    """
    Test Rate conversion
    """

    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
        """
        setup test environment
        """
        settings.RATE_SERVICE = 'forex'
        from_date = datetime.date(year=2020, month=7, day=20)
        to_date = datetime.date(year=2020, month=7, day=25)
        Rate.objects.fetch_rates(base_currency=self.base_currency, date_obj=from_date,
                                 to_obj=to_date)
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.converter = RateConverter(user=self.user, base_currency='EUR')
        self.amounts = [
            {
                'currency': 'USD',
                'amount': 100,
                'date_obj': '2020-07-22'
            },
            {
                'currency': 'AUD',
                'amount': 50,
                'date_obj': '2020-07-23'
            },
        ]
        self.trash_amounts = [
            {
                'currency': 'USD',
                'amount': 'toto',
                'date_obj': '01/01/2020'
            },
            {
                'currency': 'LOL',
                'date_obj': '2020-07-23'
            },
            {
                'date_obj': '2020-07-23'
            },
            {
                'currency': 'JPY',
            },
        ]

    def test_created(self):
        """
        Test converter initial status
        """
        self.assertEqual(self.converter.status, self.converter.INITIATED_STATUS)

    def test_add_data(self):
        """
        Test adding data to a converter
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        errors = self.converter.add_data(self.amounts)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status, self.converter.INSERTING_STATUS)
        self.assertIsNotNone(self.converter.cached_currencies)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_amounts(self):
        """
        Test adding trash data to the converter
        """
        converter = RateConverter(user=self.user, base_currency='EUR')
        errors = converter.add_data(self.trash_amounts)
        self.assertEqual(len(errors), 4)
        self.assertIn("amount", errors[0])
        self.assertIn("currency", errors[1])
        self.assertNotIn("date_obj", errors[2])
        self.assertNotIn("currency", errors[3])

    def test_convert(self):
        """
        Conversion test
        """
        result = self.converter.convert()
        self.assertEqual(result.id, self.converter.id)
        self.assertEqual(result.target, 'EUR')
        self.assertEqual(self.converter.status, self.converter.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)

    def test_convert_pivot(self):
        """
        Test converting currencies with indirect relation
        """
        Rate.objects.fetch_rates(base_currency='EUR', currency='AUD',
                                 date_obj=datetime.date(year=2020, month=7, day=23))
        Rate.objects.fetch_rates(base_currency='JPY', currency='EUR',
                                 date_obj=datetime.date(year=2020, month=7, day=23))
        converter = RateConverter(self.user, base_currency='JPY')
        amounts = [
            {
                'currency': 'AUD',
                'amount': 50,
                'date_obj': '2020-07-23'
            },
        ]
        converter.add_data(amounts)
        result = converter.convert()
        self.assertEqual(result.id, converter.id)
        self.assertEqual(result.target, 'JPY')
        self.assertEqual(converter.status, converter.FINISHED)
        self.assertEqual(result.errors, [])
        self.assertEqual(len(result.detail), len(converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)


class RateConverterAPITest(TestCase):
    """
    Test Rate conversion API
    """

    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
        """
        setup test environment
        """
        settings.RATE_SERVICE = 'forex'
        from_date = datetime.date(year=2020, month=7, day=20)
        to_date = datetime.date(year=2020, month=7, day=25)
        Rate.objects.fetch_rates(base_currency=self.base_currency, date_obj=from_date,
                                 to_obj=to_date)
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.converter = RateConverter(user=self.user, base_currency='EUR')
        self.amounts = [
            {
                'currency': 'USD',
                'amount': 100,
                'date_obj': '2020-07-22'
            },
            {
                'currency': 'AUD',
                'amount': 50,
                'date_obj': '2020-07-23'
            },
        ]
        self.trash_amounts = [
            {
                'currency': 'USD',
                'amount': 'toto',
                'date_obj': '01/01/2020'
            },
            {
                'currency': 'LOL',
                'date_obj': '2020-07-23'
            },
            {
                'date_obj': '2020-07-23'
            },
            {
                'currency': 'JPY',
            },
        ]

    def test_convert_request(self):
        """
        Test conversion request
        """
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        amounts = RateAmountSerializer(self.amounts, many=True)
        client = APIClient()
        response = client.post(
            '/rates/convert/',
            data={
                'data': amounts.data,
                'target': 'EUR',
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sum', response.json())
        self.assertEqual(len(response.json().get('detail')), len(self.amounts))

    def test_convert_batch_request(self):
        """
        Test batch conversion
        """
        batch_id = uuid.uuid4()
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        client = APIClient()
        amounts = RateAmountSerializer(self.amounts, many=True)
        response = client.post(
            '/rates/convert/',
            data={
                'data': amounts.data,
                'target': 'EUR',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), RateConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.post(
            '/rates/convert/',
            data={
                'data': amounts.data,
                'batch_id': batch_id,
                'target': 'EUR',
                'eob': True
            },
            format='json')
        self.assertEqual(response.json().get('status'), RateConverter.FINISHED)
        self.assertEqual(len(response.json().get('detail')), 2 * len(self.amounts))

    def test_watch_request(self):
        """
        Test observation of the batch
        """
        batch_id = uuid.uuid4()
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        client = APIClient()
        amounts = RateAmountSerializer(self.amounts, many=True)
        response = client.post(
            '/rates/convert/',
            data={
                'data': amounts.data,
                'target': 'EUR',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), RateConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.get(
            f'/watch/{str(batch_id)}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'), RateConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
