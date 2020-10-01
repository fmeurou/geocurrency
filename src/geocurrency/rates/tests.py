import datetime
import uuid

from datetime import date
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Rate, RateConverter
from .serializers import RateAmountSerializer


class RateTest(TestCase):
    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
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
        rates = Rate.objects.fetch_rates(base_currency=self.base_currency)
        self.assertIsNotNone(rates)

    def test_fetch_rates_with_date(self):
        rates = Rate.objects.fetch_rates(base_currency=self.base_currency, date_obj=date(year=2020, month=6, day=1))
        self.assertIsNotNone(rates)

    def test_fetch_rate(self):
        rate = Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate)

    def test_fetch_rate_with_date(self):
        rate = Rate.objects.fetch_rates(
            base_currency=self.base_currency, currency=self.currency,
            date_obj=date(year=2020, month=6, day=1)
        )
        self.assertIsNotNone(rate)

    def test_find_direct_rate(self):
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        rate = Rate.objects.find_direct_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate, msg="no direct rate found")

    def test_find_pivot_rate(self):
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        rate = Rate.objects.find_pivot_rate(base_currency=self.base_currency, currency='AUD')
        self.assertIsNotNone(rate, msg="no pivot rate found")

    def test_rate_at_date(self):
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        Rate.objects.fetch_rates(base_currency=self.currency, currency='AUD')
        rate = Rate.objects.find_direct_rate(base_currency=self.base_currency, currency=self.currency)
        self.assertIsNotNone(rate.pk, msg="no direct rate found")
        rate = Rate.objects.find_pivot_rate(base_currency=self.base_currency, currency='AUD')
        self.assertIsNotNone(rate.pk, msg="no pivot rate found")

    def test_post_rate(self):
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
        self.assertEqual(len(response.json()), 2)

    def test_post_rate_without_key(self):
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
        Rate.objects.fetch_rates(base_currency=self.base_currency, currency=self.currency)
        client = APIClient()
        response = client.get(
            '/rates/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_connected_list_request(self):
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
        self.assertEqual(len(response.json()), len(anon_response.json()) + 2)

    def test_list_user_request(self):
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
        self.assertEqual(len(response.json()), len(anon_response.json()) + 2)

    def test_list_with_key_request(self):
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
        self.assertEqual(len(response.json()), 2)

    def test_list_with_key_and_currency_request(self):
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
        self.assertEqual(len(response.json()), 1)

    def test_list_with_key_and_base_currency_request(self):
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
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get(
            '/rates/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bulk_create_request(self):
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
                         (datetime.date(year=2020, month=9, day=1) - datetime.date(year=2020, month=1, day=1)).days + 1)

    def test_latest_currency_request(self):
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
        self.assertEqual(len(response.json()), 1)
        response = client.get(
            '/rates/?base_currency_latest_values=EUR'
        )
        self.assertEqual(len(response.json()), 1)


class RateConverterTest(TestCase):
    base_currency = 'EUR'
    currency = 'USD'

    def setUp(self) -> None:
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
        self.assertEqual(self.converter.status, self.converter.INITIATED_STATUS)

    def test_add_data(self):
        errors = self.converter.add_data(self.amounts)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status, self.converter.INSERTING_STATUS)
        self.assertIsNotNone(self.converter.cached_currencies)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_amounts(self):
        converter = RateConverter(user=self.user, base_currency='EUR')
        errors = converter.add_data(self.trash_amounts)
        self.assertEqual(len(errors), 4)
        self.assertIn("amount", errors[0])
        self.assertIn("currency", errors[1])
        self.assertNotIn("date_obj", errors[2])
        self.assertNotIn("currency", errors[3])

    def test_convert(self):
        result = self.converter.convert()
        self.assertEqual(result.id, self.converter.id)
        self.assertEqual(result.target, 'EUR')
        self.assertEqual(self.converter.status, self.converter.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)

    def test_convert_pivot(self):
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

    def test_convert_request(self):
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
