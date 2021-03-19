"""
Core helpers
"""
from importlib import import_module

import logging
from django.apps import apps
from django.conf import settings


def service(service_type: str, service_name: str, *args, **kwargs):
    """
    Service wrapper
    Services are used to abstract calls to external services
    """
    service_path = settings.SERVICES[service_type][service_name]
    if not hasattr(apps, 'services'):
        setattr(apps, 'services', {})
    if service_name in apps.services:
        return apps.services.get(service_name)
    try:
        service = service_path.split('.')
        module_name = '.'.join(service[:-1])
        class_name = service[-1]
        module = import_module(module_name)
        service_class = getattr(module, class_name)
        service = service_class(*args, **kwargs)
        apps.services[service_name] = service
        return service
    except (AttributeError, ImportError, KeyError) as e:
        logging.error(e)
        return None


def validate_language(lang):
    """
    Validate languages based on settings
    """
    if lang in [l[0] for l in settings.LANGUAGES]:
        return lang
    return 'en'