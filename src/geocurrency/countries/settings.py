"""
Settings specific to Country module
"""

FLAG_SOURCE = 'https://raw.githubusercontent.com/cristiroma/countries' \
              '/master/data/flags/SVG/{alpha_2}.svg?sanitize=true'

# put in global settings.py to override
GEOCODING_SERVICE = 'pelias'

# put in global settings.py to override
GEOCODER_PELIAS_URL = 'https://api.geocode.earth/v1'
GEOCODER_PELIAS_KEY = ''
GEOCODER_GOOGLE_KEY = ''

GEOCODING_SERVICE_SETTINGS = {
    'pelias': {
        'class': 'geocurrencies.countries.services.pelias',
        'default_url': 'http://127.0.0.1:3100/v1',
        'reverse': {
            'service': 'reverse',
        },
        'search': {
            'service': 'search',  # path of the search service
            'address': 'text'
        }

    },
    'google': {
        'class': 'geocurrencies.countries.services.google',
        'default_url': 'https://maps.googleapis.com/maps/api',
        'reverse': {
            'service': 'reverse/json',
        },
        'search': {
            'service': 'geocode/json',  # Path of the search service
            'address': 'address'
        }
    }

}
