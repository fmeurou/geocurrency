import requests
from lxml import etree
from django.db import IntegrityError
from .models import ConversionRate, CurrencyModel
from .settings import RATES


def import_xml_series(base, xml_tree):
    data = xml_tree.getchildren()[-1]
    series = data.getchildren()
    records = []
    for serie in series:
        date = serie.get('time')
        currencies = serie.getchildren()
        for currency in currencies:
            try:
                currency_object = CurrencyModel.objects.get(code=currency.get('currency'))
            except CurrencyModel.DoesNotExist:
                # print("Unknown currency", currency.get('currency'))
                continue
            try:
                base_currency = CurrencyModel.objects.get(code=base)
            except CurrencyModel.DoesNotExist:
                # print("Unknown currency", base)
                continue
            try:
                records.append(ConversionRate(
                    date=date,
                    currency=currency_object,
                    base_currency=base_currency,
                    rate=float(currency.get('rate'))
                ))
            except IntegrityError as e:
                print("Unable to create rate", e)
    ConversionRate.objects.bulk_create(records)


def import_rates(scope='current'):
    """
    Import rates from config
    :param scope: current for daily values, history for all values
    :return:
    """
    for base, config in RATES.items():
        resp = requests.request('GET', config[scope])
        # print(resp.text)
        xml_tree = etree.fromstring(resp.content)
        # return xml_tree
        import_xml_series(base, xml_tree)


def import_history_rates():
    return import_rates('history')


def import_current_rates():
    return import_rates('current')
