"""
Rates services
"""
from collections import Iterator

from datetime import date as dt
from django.conf import settings


class RateNotAvailableError(Exception):
    """
    Rate could not be found
    """
    pass


class RatesNotAvailableError(Exception):
    """
    Rates service is not available
    """
    pass


class RateService:
    """
    Rate service
    """
    @staticmethod
    def serializer(base_currency, currency, date, value):
        """
        Serialize rate from service
        """
        return {
            'base_currency': base_currency,
            'currency': currency,
            'date': date,
            'value': value
        }

    def available_currencies(self) -> Iterator:
        """
        Return list of avalaible currencies
        """
        raise NotImplementedError

    def fetch_rates(self,
                    base_currency: str = settings.BASE_CURRENCY,
                    currency: str = None,
                    date_obj: dt = dt.today(),
                    to_obj: dt = None) -> []:
        """
        Get rates for a base currency at a given date
        :param base_currency: Base currency
        :param currency: currency
        :param date_obj: Date of value
        :param to_obj: Optional range of values
        :return: List of dicts [{'base_currency': base currency,
            'currency': currency, 'date': date of value, 'value'}]
        """
        raise NotImplementedError
