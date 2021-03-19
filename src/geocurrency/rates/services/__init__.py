"""
Rates services
"""
from collections import Iterator

from datetime import date
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

    def serializer(self, base_currency, currency, date, value):
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
                    date_obj: date = date.today(),
                    to_obj: date = None) -> []:
        """
        Get rates for a base currency at a given date
        :param base_currency: Base currency
        :param date_obj: Date of value
        :param to_obj: Optional range of values
        :return: List of dicts [{'base_currency': base currency, 'currency': currency, 'date': date of value, 'value'}]
        """
        raise NotImplementedError
