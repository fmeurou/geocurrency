import logging

import requests
from django.conf import settings
from pycountry import countries

from . import Geocoder
from ..settings import *


class PeliasGeocoder(Geocoder):
    coder_type = 'pelias'
    server_url = None
    key = None

    def __new__(cls, *args, **kwargs):
        return super(Geocoder, cls).__new__(cls)

    def __init__(self, server_url=None, key=None, *args, **kwargs):
        """
        Init pelias geocoder
        Init: Geocoder('pelias', server_url='serveur URL', key='API key')
        :params server_url: Custom pelias URL, defaults to 'https://api.geocode.earth/v1/search'
        :param key: API key
        """
        self.key = key or settings.GEOCODER_PELIAS_KEY
        try:
            pelias_url = settings.GEOCODER_PELIAS_URL
        except AttributeError:
            pelias_url = GEOCODING_SERVICE_SETTINGS['pelias']['default_url']
        self.server_url = server_url or pelias_url

    def search(self, address, language=None, bounds=None, region=None, components=""):
        search_args = {'text': address}
        if self.key:
            search_args['api_key'] = self.key
        try:
            response = requests.get(f'{self.server_url}/search', search_args)
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
        search_args = {
            'point.lat': lat,
            'point.lon': lng,
        }
        if self.key:
            search_args['api_key'] = self.key
        try:
            response = requests.get(f'{self.server_url}/reverse', search_args)
            data = response.json()
            if 'errors' in data:
                logging.error("ERROR - Invalid request")
                logging.error(data.get('error'))
                return None
            return data
        except ValueError as e:
            logging.error("Invalid API configuration")
            logging.error(e)
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
