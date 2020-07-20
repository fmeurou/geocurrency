import os
from django.conf import settings
from django.test import TestCase

from .models import Geocoder

PELIAS_TEST_URL = 'http://api.geocurrency.me:3100/v1'
TEST_ADDRESS = "Avenue de la Division Leclerc, 92310 Sèvres"
TEST_LAT = 48.763434
TEST_LNG = 2.308702


class GeocoderTestCase(TestCase):

    def setUp(self) -> None:
        settings.GOOGLE_GEOCODER = True
        settings.PELIAS_GEOCODER = True
        settings.GOOGLE_GEOCODER_KEY = os.environ.get('GOOGLE_API_KEY')
        settings.PELIAS_GEOCODER_URL = PELIAS_TEST_URL

    def test_google(self) ->None:
        if settings.GOOGLE_GEOCODER_KEY:
            geocoder = Geocoder(coder_type='google', key=settings.GOOGLE_GEOCODER_KEY)
            self.assertEqual(geocoder.coder_type, 'google')
        else:
            with self.assertRaises(ValueError):
                Geocoder(coder_type='google')

    def test_pelias(self):
        geocoder = Geocoder(coder_type='pelias')
        self.assertEqual(geocoder.coder_type, 'pelias')

    def test_google_search(self):
        if settings.GOOGLE_GEOCODER_KEY:
            geocoder = Geocoder(coder_type='google', key=settings.GOOGLE_GEOCODER_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
        else:
            self.assertTrue(False)

    def test_google_reverse(self):
        if settings.GOOGLE_GEOCODER_KEY:
            geocoder = Geocoder(coder_type='google', key=settings.GOOGLE_GEOCODER_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
        else:
            self.assertTrue(False)

    def test_pelias_search(self):
        geocoder = Geocoder(coder_type='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.search(address=TEST_ADDRESS)
        self.assertIsNotNone(data)

    def test_pelias_reverse(self):
        geocoder = Geocoder(coder_type='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
        self.assertIsNotNone(data)

    def test_pelias_search_parse_countries(self):
        """
        Test with pelias search
        """
        geocoder = Geocoder(coder_type='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.search(address=TEST_ADDRESS)
        self.assertIsNotNone(data)
        self.assertIn("FR", geocoder.parse_countries(data))

    def test_pelias_reverse_parse_countries(self):
        """
        Test with pelias reverse
        """
        geocoder = Geocoder(coder_type='pelias', server_url=PELIAS_TEST_URL)
        data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
        self.assertIsNotNone(data)
        if 'errors' in data:
            print("ERROR - pelias-interpolation service is not working, avoiding test")
        self.assertIn("FR", geocoder.parse_countries(data))

    def test_google_search_parse_countries(self):
        """
        Test with google search
        """
        if settings.GOOGLE_GEOCODER_KEY:
            geocoder = Geocoder(coder_type='google', key=settings.GOOGLE_GEOCODER_KEY)
            data = geocoder.search(address=TEST_ADDRESS)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            self.assertTrue(False)

    def test_google_reverse_parse_countries(self):
        """
        Test with google reverse
        """
        if settings.GOOGLE_GEOCODER_KEY:
            geocoder = Geocoder(coder_type='google', key=settings.GOOGLE_GEOCODER_KEY)
            data = geocoder.reverse(lat=TEST_LAT, lng=TEST_LNG)
            self.assertIsNotNone(data)
            self.assertIn("FR", geocoder.parse_countries(data))
        else:
            self.assertTrue(False)
