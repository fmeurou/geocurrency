import os
from django.conf import settings
from django.test import TestCase
from pycountry import countries
from rest_framework import status
from rest_framework.test import APIClient

from geocurrency.core.helpers import service

from .models import Country
from .serializers import CountrySerializer

PELIAS_TEST_URL = 'http://api.geocurrency.me:3100/v1'
TEST_ADDRESS = "Avenue de la Division Leclerc, 92310 Sèvres"
TEST_LAT = 48.763434
TEST_LNG = 2.308702


class CountryTestCase(TestCase):

    def setUp(self) -> None:
        settings.GEOCODING_SERVICE = 'google'
        settings.GEOCODER_GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')

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
        self.assertEqual(country.unit_system, 'SI')

    def test_unit_system(self):
        self.assertEqual(Country('FR').unit_system, 'SI')
        self.assertEqual(Country('US').unit_system, 'US')
        self.assertEqual(Country('LR').unit_system, 'US')
        self.assertEqual(Country('MM').unit_system, 'imperial')

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.all_countries()))
        self.assertEqual(response.data[0].get('alpha_2'), 'AW')

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get('/countries/US/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cs = CountrySerializer(data=response.json())
        self.assertTrue(cs.is_valid())
        country = cs.create(cs.validated_data)
        self.assertEqual(country.name, 'United States')
        self.assertEqual(country.region, 'Americas')
        self.assertEqual(country.subregion, 'Northern America')
        self.assertEqual(country.unit_system, 'US')

    def test_google_geocode_request(self):
        client = APIClient()
        response = client.get(
            '/countries/geocode/',
            data={'address': TEST_ADDRESS, 'key': settings.GEOCODER_GOOGLE_KEY},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_google_reverse_request(self):
        client = APIClient()
        response = client.get(
            '/countries/reverse/',
            data={'lat': TEST_LAT, 'lon': TEST_LNG, 'key': settings.GEOCODER_GOOGLE_KEY},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_timezones_request(self):
        client = APIClient()
        response = client.get('/countries/FR/timezones/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_currencies_request(self):
        client = APIClient()
        response = client.get('/countries/FR/currencies/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "EUR")

    def test_provinces_request(self):
        client = APIClient()
        response = client.get('/countries/FR/provinces/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Alsace")

    def test_languages_request(self):
        client = APIClient()
        response = client.get('/countries/FR/languages/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "fr")

    def test_colors_request(self):
        client = APIClient()
        response = client.get('/countries/FR/colors/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borders_request(self):
        client = APIClient()
        response = client.get('/countries/FR/borders/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "DEU")


class GeocoderTestCase(TestCase):

    def setUp(self) -> None:
        settings.GEOCODER_GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
        settings.PELIAS_GEOCODER_URL = PELIAS_TEST_URL

    def test_google(self) -> None:
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google', key=settings.GEOCODER_GOOGLE_KEY)
            self.assertEqual(geocoder.coder_type, 'google')
        else:
            with self.assertRaises(ValueError):
                service(service_type='geocoding', service_name='google')

    def test_pelias(self):
        geocoder = service(service_type='geocoding', service_name='pelias')
        self.assertEqual(geocoder.coder_type, 'pelias')

    def test_google_search(self):
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google', key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
        else:
            self.assertTrue(False)

    def test_google_reverse(self):
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google', key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
        else:
            self.assertTrue(False)

    def test_pelias_search(self):
        geocoder = service(service_type='geocoding', service_name='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.search(address=TEST_ADDRESS)
        self.assertIsNotNone(data)

    def test_pelias_reverse(self):
        geocoder = service(service_type='geocoding', service_name='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
        self.assertIsNotNone(data)

    def test_pelias_search_parse_countries(self):
        """
        Test with pelias search
        """
        geocoder = service(service_type='geocoding', service_name='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.search(address=TEST_ADDRESS)
        self.assertIsNotNone(data)
        self.assertIn("FR", geocoder.parse_countries(data))

    def test_pelias_reverse_parse_countries(self):
        """
        Test with pelias reverse
        """
        geocoder = service(service_type='geocoding', service_name='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
        self.assertIsNotNone(data)
        if 'errors' in data:
            print("ERROR - pelias-interpolation service is not working, avoiding test")
            return
        self.assertIn("FR", geocoder.parse_countries(data))

    def test_google_search_parse_countries(self):
        """
        Test with google search
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google', key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            self.assertTrue(False)

    def test_google_reverse_parse_countries(self):
        """
        Test with google reverse
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google', key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            self.assertTrue(False)
