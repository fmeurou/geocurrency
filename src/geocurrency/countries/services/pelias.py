import logging
import requests
from django.conf import settings
from pycountry import countries

from . import Geocoder
from ..settings import *


class PeliasGeocoder(Geocoder):
    coder_type = 'pelias'
    server_url = None

    def __init__(self, server_url=None, *args, **kwargs):
        """
        Init pelias geocoder
        :params server_url: Custom pelias URL, defaults to 'http://127.0.0.1:3100/v1'
        """
        try:
            pelias_url = settings.PELIAS_GEOCODER_URL
        except AttributeError:
            pelias_url = GEOCODING_SERVICE_SETTINGS['pelias']['default_url']
        self.server_url = server_url or pelias_url

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
