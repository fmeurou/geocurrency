import logging
import json
import requests

from . import Geocoder
from ..settings import *
from django.conf import settings


GEOCODER_GOOGLE_URL = 'https://maps.googleapis.com/maps/api'


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
            if not key or not settings.GEOCODER_GOOGLE_KEY:
                raise ValueError(
                    "This geocoder needs an API key, please provide a key or set GEOCODER_GOOGLE_KEY in configuration")
        except AttributeError:
            raise ValueError(
                "This geocoder needs an API key, please provide a key or set GEOCODER_GOOGLE_KEY in configuration")
        self.key = key or settings.GEOCODER_GOOGLE_KEY

    def search(self, address, language=None, bounds=None, region=None, components=""):
        """
        Google geocoding search
        Retrieves coordinates based on address
        """
        try:
            response = requests.get('{}/{}'.format(
                GEOCODER_GOOGLE_URL,
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
                GEOCODER_GOOGLE_URL,
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
