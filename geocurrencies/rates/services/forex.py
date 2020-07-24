# Python_forex based wrapper
# uses ratesapi.io
import logging
from datetime import date, timedelta
from django.conf import settings
from forex_python import converter
from typing import Iterator

from . import RateService, RatesNotAvailableError


class ForexService(RateService):

    def available_currencies(self) -> Iterator:
        rates = self.fetch_rates(base_currency='USD')
        return [r['currency'] for r in rates]

    def _fetch_all_rates(self, provider: converter.CurrencyRates, base_currency: str, date_obj: date) -> []:
        try:
            _rates = provider.get_rates(base_cur=base_currency, date_obj=date_obj)
            return [self.serializer(
                base_currency=base_currency,
                currency=key,
                date=date_obj,
                value=value
            ) for key, value in _rates.items()]
        except converter.RatesNotAvailableError as e:
            logging.error(e)
            raise RatesNotAvailableError

    def _fetch_single_rate(self,
                           provider: converter.CurrencyRates,
                           base_currency: str,
                           currency: str, date_obj: date) -> []:
        try:
            value = provider.get_rate(dest_cur=currency, base_cur=base_currency, date_obj=date_obj)
            return [self.serializer(
                base_currency=base_currency,
                currency=currency,
                date=date_obj,
                value=value
            )]

        except converter.RatesNotAvailableError as e:
            logging.error(e)
            raise RatesNotAvailableError

    def fetch_rates(self,
                    base_currency: str = settings.BASE_CURRENCY,
                    currency: str = None,
                    date_obj: date = date.today(), to_obj: date = None) -> []:
        c = converter.CurrencyRates()
        rates = []
        _rates = []
        if currency:
            for i in range(((to_obj or date_obj) - date_obj).days + 1):
                _rates = self._fetch_single_rate(c, base_currency=base_currency, currency=currency,
                                                 date_obj=date_obj + timedelta(i))
                rates.extend(_rates)
        else:
            for i in range(((to_obj or date_obj) - date_obj).days + 1):
                _rates = self._fetch_all_rates(c, base_currency=base_currency, date_obj=date_obj + timedelta(i))
                rates.extend(_rates)
        return rates
