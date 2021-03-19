"""
Country tests
"""
import os

from django.conf import settings
from django.test import TestCase
from geocurrency.core.helpers import service
from pycountry import countries
from rest_framework import status
from rest_framework.test import APIClient

from .models import Country
from .serializers import CountrySerializer

PELIAS_TEST_URL = 'https://api.geocode.earth/v1'
TEST_ADDRESS = "Rue du Maine, 75014 Paris"
TEST_LAT = 48.763434
TEST_LNG = 2.308702


class CountryTestCase(TestCase):
    """
    Test Country object
    """

    def setUp(self) -> None:
        """
        Set test up
        """
        settings.GEOCODING_SERVICE = 'google'
        settings.GEOCODER_GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
        settings.GEOCODER_PELIAS_KEY = os.environ.get('PELIAS_API_KEY')

    def test_all(self):
        """Numbers of countries is equal to number of countries in pycountry.countries"""
        all_countries = Country.all_countries()
        self.assertEqual(len(list(all_countries)), len(countries))

    def test_sorted_all(self):
        """Numbers of countries is equal to number of countries in pycountry.countries"""
        self.assertEqual(len(list(Country.all_countries())), len(countries))
        self.assertEqual(Country.all_countries(ordering='name')[-1].alpha_2, 'AX')
        self.assertEqual(Country.all_countries(ordering='alpha_2')[-1].alpha_2, 'ZW')
        self.assertEqual(Country.all_countries(ordering='alpha_3')[-1].alpha_2, 'ZW')
        self.assertEqual(Country.all_countries(ordering='numeric')[-1].alpha_2, 'ZM')
        self.assertEqual(Country.all_countries(ordering='brouzouf')[-1].alpha_2, 'AX')

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
        """
        Check unit systems (only US and UK have strange unit systems
        """
        self.assertEqual(Country('FR').unit_system, 'SI')
        self.assertEqual(Country('US').unit_system, 'US')
        self.assertEqual(Country('LR').unit_system, 'US')
        self.assertEqual(Country('MM').unit_system, 'imperial')

    def test_flag_path(self):
        """
        Looking for flags
        """
        country = Country('FR')
        self.assertEqual(country.flag_path,
                         os.path.join(settings.MEDIA_ROOT, country.alpha_2 + '.svg'))

    def test_flag_exists_and_download(self):
        """
        Testing that flag can be downloaded
        """
        country = Country('FR')
        os.remove(country.flag_path)
        self.assertFalse(country.flag_exists())
        self.assertIsNotNone(country.download_flag())
        self.assertTrue(country.flag_exists())

    def test_colors(self):
        """
        Testing colors have been parsed
        """
        country = Country('FR')
        self.assertIsNotNone(country.colors())


class CountryAPITestCase(TestCase):
    """
    Country API tests
    """

    def setUp(self) -> None:
        """
        Set test up
        """
        settings.GEOCODING_SERVICE = 'google'
        settings.GEOCODER_GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
        settings.GEOCODER_PELIAS_KEY = os.environ.get('PELIAS_API_KEY')

    def test_list_request(self):
        """
        Testing the list of countries
        """
        client = APIClient()
        response = client.get('/countries/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.all_countries()))
        self.assertEqual(response.data[0].get('alpha_2'), 'AF')

    def test_list_sorted_name_request(self):
        """
        testing name ordering on List API
        """
        client = APIClient()
        response = client.get('/countries/', data={'ordering': 'name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.all_countries()))
        self.assertEqual(response.data[-1].get('alpha_2'), 'AX')

    def test_list_sorted_numeric_request(self):
        """
        testing numeric ordering on List API
        """
        client = APIClient()
        response = client.get('/countries/', data={'ordering': 'numeric'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.all_countries()))
        self.assertEqual(response.data[-1].get('alpha_2'), 'ZM')

    def test_retrieve_request(self):
        """
        Testing retieve on country
        """
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
        """
        Testing geocoding from google
        """
        if settings.GEOCODER_GOOGLE_KEY:
            client = APIClient()
            response = client.get(
                '/countries/geocode/',
                data={'address': TEST_ADDRESS, 'key': settings.GEOCODER_GOOGLE_KEY},
                format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")

    def test_google_reverse_request(self):
        """
        Testing reverse from google
        """
        if settings.GEOCODER_GOOGLE_KEY:
            client = APIClient()
            response = client.get(
                '/countries/reverse/',
                data={'lat': TEST_LAT, 'lon': TEST_LNG, 'key': settings.GEOCODER_GOOGLE_KEY},
                format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")

    def test_timezones_request(self):
        """
        Testing timezone information
        """
        client = APIClient()
        response = client.get('/countries/FR/timezones/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_currencies_request(self):
        """
        Testing currencies information
        """
        client = APIClient()
        response = client.get('/countries/FR/currencies/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "EUR")

    def test_provinces_request(self):
        """
        Testing provingces information
        """
        client = APIClient()
        response = client.get('/countries/FR/provinces/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Alsace")

    def test_languages_request(self):
        """
        Testing languages information
        """
        client = APIClient()
        response = client.get('/countries/FR/languages/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "fr")

    def test_colors_request(self):
        """
        Testing colors information
        """
        client = APIClient()
        response = client.get('/countries/FR/colors/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borders_request(self):
        """
        Testing borders information
        """
        client = APIClient()
        response = client.get('/countries/FR/borders/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "DEU")


class GeocoderTestCase(TestCase):
    """
    Testing geocoders
    """

    def setUp(self) -> None:
        settings.GEOCODER_GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
        settings.GEOCODER_PELIAS_KEY = os.environ.get('PELIAS_API_KEY')
        settings.PELIAS_GEOCODER_URL = PELIAS_TEST_URL

    def test_google(self) -> None:
        """
        Testing Google service
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google',
                               key=settings.GEOCODER_GOOGLE_KEY)
            self.assertEqual(geocoder.coder_type, 'google')
        else:
            with self.assertRaises(ValueError):
                service(service_type='geocoding', service_name='google')

    def test_pelias(self):
        """
        Testing Pelias service
        """
        if settings.GEOCODER_PELIAS_KEY:
            geocoder = service(service_type='geocoding', service_name='pelias',
                               server_url=PELIAS_TEST_URL,
                               key=settings.GEOCODER_PELIAS_KEY)
            self.assertEqual(geocoder.coder_type, 'pelias')
        else:
            print("GEOCODER_PELIAS_KEY not set, skipping test")

    def test_google_search(self):
        """
        Testing Google geocoding
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google',
                               key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")

    def test_google_reverse(self):
        """
        Testing Google revrese geocoding
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google',
                               key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")

    def test_pelias_search(self):
        """
        Testing Pelias geocoding
        """
        if settings.GEOCODER_PELIAS_KEY:
            geocoder = service(service_type='geocoding', service_name='pelias',
                               server_url=PELIAS_TEST_URL,
                               key=settings.GEOCODER_PELIAS_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
        else:
            print("GEOCODER_PELIAS_KEY not set, skipping test")

    def test_pelias_reverse(self):
        """
        Testing Pelias reverse geocoding
        """
        if settings.GEOCODER_PELIAS_KEY:
            geocoder = service(service_type='geocoding', service_name='pelias',
                               server_url=PELIAS_TEST_URL,
                               key=settings.GEOCODER_PELIAS_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
        else:
            print("GEOCODER_PELIAS_KEY not set, skipping test")

    def test_pelias_search_parse_countries(self):
        """
        Test with pelias search
        """
        if settings.GEOCODER_PELIAS_KEY:
            geocoder = service(service_type='geocoding', service_name='pelias',
                               server_url=PELIAS_TEST_URL,
                               key=settings.GEOCODER_PELIAS_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            print("GEOCODER_PELIAS_KEY not set, skipping test")

    def test_pelias_reverse_parse_countries(self):
        """
        Test with pelias reverse
        """
        if settings.GEOCODER_PELIAS_KEY:
            geocoder = service(service_type='geocoding', service_name='pelias',
                               server_url=PELIAS_TEST_URL,
                               key=settings.GEOCODER_PELIAS_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
            if 'errors' in data:
                print("ERROR - Pelias service not available")
                return
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            print("GEOCODER_PELIAS_KEY not set, skipping test")

    def test_google_search_parse_countries(self):
        """
        Test with google search
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google',
                               key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")

    def test_google_reverse_parse_countries(self):
        """
        Test with google reverse
        """
        if settings.GEOCODER_GOOGLE_KEY:
            geocoder = service(service_type='geocoding', service_name='google',
                               key=settings.GEOCODER_GOOGLE_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            print("GEOCODER_GOOGLE_KEY not set, skipping test")
