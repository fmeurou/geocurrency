import json
import logging
import requests
from django.conf import settings
from pycountry import countries
from timezonefinder import TimezoneFinder

from .settings import *

GOOGLE_GEOCODER_URL = 'https://maps.googleapis.com/maps/api'

from ..countries.models import Country

tf = TimezoneFinder(in_memory=True)


class Geocoder:

    def __new__(cls, coder_type=None, *args, **kwargs):
        try:
            selected_api = settings.GEOCODING_API
        except AttributeError:
            selected_api = GEOCODING_API

        if not coder_type:
            coder_type = selected_api
        if coder_type == 'pelias' and settings.PELIAS_GEOCODER:
            return PeliasGeoCoder(*args, **kwargs)
        elif coder_type == 'google' and settings.GOOGLE_GEOCODER:
            return GoogleGeocoder(*args, **kwargs)
        else:
            raise ValueError("Invalid geocoder")

    def search(self, address, language=None, bounds=None, region=None, components=""):
        """
        :params text: address to search for
        :params language: optional, language of result
        :params bounds: optional, limit results to bounds
        :params region: optional, limit results to region
        :params components: optional, a components filter with elements separated by a pipe (|)
        :returns: Country
        """
        raise NotImplementedError("Use specific implementation")

    def reverse(self, lat, lng):
        """
        :params lat: latitude
        :params lng: longitude
        """
        raise NotImplementedError("Use specific implementation")

    def parse_countries(self, data):
        """
        :params data: geocoding / reverse geocoding result
        :returns: Country instance
        """
        raise NotImplementedError("Use specific implementation")

    def countries(self, data):
        """
        :params data: json response from geocoding / reverse geocoding service
        """
        countries = []
        alphas = self.parse_countries(data=data)
        for alpha in alphas:
            try:
                if len(alpha) == 2:
                    country = Country(alpha)
                elif len(alpha) == 3:
                    country = Country(alpha[0:2])
                else:
                    country = Country(alpha)
            except KeyError:
                continue
            countries.append(country)
        return countries


class PeliasGeoCoder(Geocoder):
    coder_type = 'pelias'
    server_url = None

    def __new__(cls, *args, **kwargs):
        return super(Geocoder, cls).__new__(cls)

    def __init__(self, server_url=None, *args, **kwargs):
        """
        Init pelias geocoder
        :params server_url: Custom pelias URL, defaults to 'http://127.0.0.1:3100/v1'
        """
        try:
            PELIAS_GEOCODER_URL = settings.PELIAS_GEOCODER_URL
        except AttributeError:
            PELIAS_GEOCODER_URL = GEOCODING_API_SETTINGS['pelias']['default_url']
        self.server_url = server_url or PELIAS_GEOCODER_URL

    def search(self, address, language=None, bounds=None, region=None, components=""):
        try:
            response = requests.get('{}/{}'.format(
                self.server_url,
                'search'

            ), {'text': address})
            data = response.json()
            if 'errors' in data:
                logging.error("Invalid request")
                logging.error(data.get('error'))
                return None
            return data
        except ValueError as e:
            logging.error("Invalid API configuration")
            logging.error(e)
        except IOError as e:
            logging.error("Invalid request")
            logging.error(e)
        return None

    def reverse(self, lat, lng):
        try:
            response = requests.get('{}/{}'.format(
                self.server_url,
                'reverse'
            ),
                {
                    'point.lat': lat,
                    'point.lon': lng,
                })
            data = response.json()
            if 'errors' in data:
                logging.error("ERROR - Invalid request")
                logging.error(data.get('error'))
                return None
            return data
        except ValueError:
            logging.error("Invalid API configuration")
        except IOError as e:
            logging.error("Invalid request", e)
        return None

    def parse_countries(self, data):
        """
        parse response from google service
        :params data: geocoding / reverse geocoding json
        :return: array of alpha2 codes
        """
        alphas = []
        if not data:
            return alphas
        for feature in data.get('features'):
            alphas.append(countries.get(alpha_3=feature.get('properties').get('country_a')).alpha_2)
        return alphas


class GoogleGeocoder(Geocoder):
    coder_type = 'google'
    key = None

    def __new__(cls, *args, **kwargs):
        return super(Geocoder, cls).__new__(cls)

    def __init__(self, key=None, *args, **kwargs):
        """
        Google geocode engine
        Init: Geocoder('google', 'API key')
        """
        try:
            if not key or not settings.GOOGLE_GEOCODER_KEY:
                raise ValueError(
                    "This geocoder needs an API key, please provide a key or set GOOGLE_GEOCODER_KEY in configuration")
        except AttributeError:
            raise ValueError(
                "This geocoder needs an API key, please provide a key or set GOOGLE_GEOCODER_KEY in configuration")
        self.key = key or GOOGLE_GEOCODER_KEY

    def search(self, address, language=None, bounds=None, region=None, components=""):
        """
        Google geocoding search
        Retrieves coordinates based on address
        """
        try:
            response = requests.get('{}/{}'.format(
                GOOGLE_GEOCODER_URL,
                'geocode/json'
            ), {
                'address': address,
                'key': self.key,
                'language': language
            })
            data = response.json()
            if data.get('status') != "OK":
                return None
            return data
        except json.JSONDecodeError as e:
            logging.error("Invalid response")
            logging.error(e)
        except ValueError as e:
            logging.error("Invalid API configuration")
            logging.error(e)
        except IOError as e:
            logging.error("Invalid request")
            logging.error(e)

        return None

    def reverse(self, lat, lng):
        """
        Google geocoding reverse
        """
        try:
            response = requests.get('{}/{}'.format(
                GOOGLE_GEOCODER_URL,
                'geocode/json'
            ),
                {
                    'latlng': ",".join(map(str, [lat, lng])),
                    'key': self.key,
                })
            data = response.json()
            if data.get('status') != "OK":
                return None
            return data
        except json.JSONDecodeError as e:
            logging.error("Invalid response")
            logging.error(e)
        except ValueError as e:
            logging.error("Invalid API configuration")
            logging.error(e)
        except IOError as e:
            logging.error("Invalid request")
            logging.error(e)
        return None

    def parse_countries(self, data):
        """
        parse response from google service
        :params data: geocoding / reverse geocoding json
        :return: array of alpha2 codes
        """
        alphas = []
        if not data:
            return alphas
        for feature in data.get('results'):
            for address_component in feature.get('address_components'):
                if 'country' in address_component.get('types'):
                    alphas.append(address_component.get('short_name'))
        return alphas


GEOCODER_CLASSES = {
    'google': GoogleGeocoder,
    'pelias': PeliasGeoCoder
}
