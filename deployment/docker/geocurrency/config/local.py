import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('GEOCURRENCY_SECRET_KEY', ''),

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'geocurrency-apis',
    os.environ.get('GEOCURRENCY_API_DOMAIN', 'api.geocurrency.me',),
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'geocurrency-apis',
    os.environ.get('GEOCURRENCY_CLIENT_DOMAIN', 'www.geocurrency.me', ),
]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('GEOCURRENCY_DB_ENGINE', 'django.db.backends.sqlite3'),
        'HOST': os.environ.get('GEOCURRENCY_DB_HOST', ''),
        'PORT': os.environ.get('GEOCURRENCY_DB_PORT', ''),
        'NAME': os.environ.get('GEOCURRENCY_DB_NAME', 'db.sqlite3'),
        'USER': os.environ.get('GEOCURRENCY_DB_USERNAME', ''),
        'PASSWORD': os.environ.get('GEOCURRENCY_DB_PASSWORD', ''),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cache:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '100000/day'
    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/apps/logs/api-debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = '/var/apps/static'
MEDIA_ROOT = '/var/apps/media'

SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = '/var/apps/media'
SENDFILE_URL = '/media'