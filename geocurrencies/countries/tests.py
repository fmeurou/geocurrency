import os
from django.conf import settings
from django.test import TestCase
from pycountry import countries
from rest_framework import status
from rest_framework.test import APIClient

from .models import Country

TEST_ADDRESS = "Avenue de la Division Leclerc, 92310 Sèvres"
TEST_LAT = 48.763434
TEST_LNG = 2.308702

class CountryTestCase(TestCase):

    def setUp(self) -> None:
        settings.GEOCODING_API = 'google'
        settings.GOOGLE_GEOCODER = True
        settings.PELIAS_GEOCODER = False
        settings.GOOGLE_GEOCODER_KEY = os.environ.get('GOOGLE_API_KEY')

    def test_all(self):
        """Numbers of countries is equal to number of countries in pycountry.countries"""
        all_countries = Country.all_countries()
        self.assertEqual(len(list(all_countries)), len(countries))

    def test_base(self):
        """
        Basic representation contains name and iso codes
        """
        country = Country("FR")
        self.assertIn("name", country.base())
        self.assertIn("alpha_2", country.base())
        self.assertIn("alpha_3", country.base())
        self.assertIn("numeric", country.base())
        self.assertEqual(country.base().get('name'), 'France')
        self.assertEqual(country.base().get('alpha_2'), 'FR')
        self.assertEqual(country.base().get('alpha_3'), 'FRA')
        self.assertEqual(country.base().get('numeric'), '250')

    def test_flag_path(self):
        country = Country('FR')
        self.assertEqual(country.flag_path, os.path.join(settings.MEDIA_ROOT, country.alpha_2 + '.svg'))

    def test_flag_exists_and_download(self):
        country = Country('FR')
        os.remove(country.flag_path)
        self.assertFalse(country.flag_exists())
        self.assertIsNotNone(country.download_flag())
        self.assertTrue(country.flag_exists())

    def test_colors(self):
        country = Country('FR')
        self.assertIsNotNone(country.colors())

    def test_list_request(self):
        client = APIClient()
        response = client.get('/countries/', format='json')
        first_country = Country.all_countries()[0].base()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.all_countries()))
        self.assertEqual(response.data[0].get('alpha_2'), 'AW')

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get('/countries/FR/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, Country('FR').info())

    def test_google_geocode_request(self):
        client = APIClient()
        response = client.get(
            '/countries/geocode/',
            data={'address': TEST_ADDRESS, 'key': settings.GOOGLE_GEOCODER_KEY},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_google_reverse_request(self):
        client = APIClient()
        response = client.get(
            '/countries/reverse/',
            data={'lat': TEST_LAT, 'lon': TEST_LNG, 'key': settings.GOOGLE_GEOCODER_KEY},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_timezones(self):
        client = APIClient()
        response = client.get('/countries/FR/timezones/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)