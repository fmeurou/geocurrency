# put in global settings.py to override
GEOCODING_API = 'pelias'

# put in global settings.py to override
PELIAS_GEOCODER = False
PELIAS_GEOCODER_URL = None

GOOGLE_GEOCODER = False
GOOGLE_GEOCODER_KEY = ''



GEOCODING_API_SETTINGS = {
    'pelias': {
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
