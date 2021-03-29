"""
Google Geocoder service
"""
import json
import logging

import requests
from django.conf import settings

from . import Geocoder

GEOCODER_GOOGLE_URL = 'https://maps.googleapis.com/maps/api'


class GoogleGeocoder(Geocoder):
    """
    Google geocoder class
    search and reverse from Google
    """
    coder_type = 'google'
    key = None

    def __new__(cls, *args, **kwargs):
        """
        Initialize
        """
        return super(Geocoder, cls).__new__(cls)

    def __init__(self, key: str = None, *args, **kwargs):
        """
        Google geocode engine
        Init: Geocoder('google', 'API key')
        """
        try:
            if not key or not settings.GEOCODER_GOOGLE_KEY:
                raise ValueError(
                    "This geocoder needs an API key, please provide a key"
                    " or set GEOCODER_GOOGLE_KEY in configuration")
        except AttributeError:
            raise ValueError(
                "This geocoder needs an API key, please provide a key "
                "or set GEOCODER_GOOGLE_KEY in configuration")
        self.key = key or settings.GEOCODER_GOOGLE_KEY

    def search(self, address: str, language: str = None, bounds=None,
               region: str = None, components: str = "") -> dict:
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
                return {}
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
        return {}

    def reverse(self, lat: str, lng: str) -> dict:
        """
        Google geocoding reverse
        :param lat: latitude
        :param lng: longitude
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
                return {}
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
        return {}

    def parse_countries(self, data: dict) -> [str]:
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
