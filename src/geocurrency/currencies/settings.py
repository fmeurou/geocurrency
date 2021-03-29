"""
Settings for Currencies module
"""

RATES = {
    'EUR': {
        'source': {
            'name': 'BCE',
            'url': 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates'
                   '/euro_reference_exchange_rates/html/index.en.html'
        },
        'history': 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml',
        'current': 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    },
    # 'CAD': {
    #     'source': {
    #       'name': 'Bank of Canada',
    #       'url': 'https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/'
    #     },
    #     'history': 'https://www.bankofcanada.ca/valet/observations
    #     /group/FX_RATES_DAILY/csv?start_date=2017-01-03',
    #     'current': 'https://www.bankofcanada.ca/valet/observations
    #     /group/FX_RATES_DAILY/csv?start_date=2017-01-03'
    # },
}

BASE_CURRENCY = 'EUR'
