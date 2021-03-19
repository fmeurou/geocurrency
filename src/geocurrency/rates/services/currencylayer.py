"""
CurrencyLayer service
"""

import requests
from datetime import date
from django.conf import settings
from typing import Iterator

from . import RatesNotAvailableError, RateService
from ..settings import *

CURRENCYLAYER_API_URL = 'http://api.currencylayer.com/'
CURRENCYLAYER_CURRENCIES_ENDPOINT = 'list'
CURRENCYLAYER_LIVE_ENDPOINT = 'live'
CURRENCYLAYER_HISTORICAL_ENDPOINT = 'historical'
CURRENCYLAYER_TIMEFRAME_ENDPOINT = 'timeframe'

try:
    CURRENCYLAYER_API_KEY = settings.CURRENCYLAYER_API_KEY
except AttributeError:
    pass


class CurrencyLayerService(RateService):
    """
    Currency layer service class
    """

    def available_currencies(self) -> Iterator:
        """
        List availbale currencies for the service
        """
        data = {
            'access_key': CURRENCYLAYER_API_KEY
        }
        url = CURRENCYLAYER_API_URL + CURRENCYLAYER_CURRENCIES_ENDPOINT
        response = requests.get(url=url, data=data)
        if response.status_code == 200:
            data = response.json()
            if 'currencies' in data:
                return data.get('currencies').keys()
            else:
                return []
        else:
            raise RatesNotAvailableError(response.text)

    def fetch_rates(self,
                    base_currency: str = settings.BASE_CURRENCY,
                    currency: str = None,
                    date_obj: date = date.today(),
                    to_obj: date = None) -> []:
        """
        Fetch rates
        :param base_currency: base currency
        :param currency: target currency
        :param date_obj: date of the rate
        :param to_obj: optional range parameter
        """
        data = {
            'access_key': CURRENCYLAYER_API_KEY,
            'source': base_currency
        }
        if currency:
            data['currencies'] = [currency]
        if date_obj == date.today():
            url = CURRENCYLAYER_API_URL + CURRENCYLAYER_LIVE_ENDPOINT
        elif to_obj:
            url = CURRENCYLAYER_API_URL + CURRENCYLAYER_HISTORICAL_ENDPOINT
            data['start_date'] = date_obj
            data['end_date'] = to_obj
        else:
            url = CURRENCYLAYER_API_URL + CURRENCYLAYER_HISTORICAL_ENDPOINT
            data['date'] = date_obj
        response = requests.get(url=url, data=data)
        if response.status_code == 200:
            data = response.json()
            if 'quotes' in data:
                return self.parse_result(base_currency=base_currency, data=data.get('quotes'))
            else:
                return {}
        else:
            raise RatesNotAvailableError(response.text)

    def parse_result(self, base_currency, data: dict) -> []:
        """
        Parse output from currencylayout services
        :param base_currency: base currency
        :param data: dictionnary of data
        """
        output = []
        if 'timeframe' in data:
            # request is timeframe based, so data is agregated by date
            for date_obj, rate_dict in data:
                for code, value in rate_dict:
                    output.append(
                        self.serializer(
                            base_currency=base_currency,
                            currency=code[3:],
                            value=value,
                            date=date_obj)
                    )
        else:
            if 'date' in data:
                # Historical search
                date_obj = data['date']
            else:
                # live search
                date_obj = date.today()
            for code, value in data:
                output.append(
                    self.serializer(
                        base_currency=base_currency,
                        currency=code[3:],
                        value=value,
                        date=date_obj
                    )
                )
        return output
