"""
Core helpers
"""
import logging
from importlib import import_module

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
        srv = service_path.split('.')
        module_name = '.'.join(srv[:-1])
        class_name = srv[-1]
        module = import_module(module_name)
        service_class = getattr(module, class_name)
        srv = service_class(*args, **kwargs)
        apps.services[service_name] = srv
        return srv
    except (AttributeError, ImportError, KeyError) as e:
        logging.error(e)
        return None


def validate_language(lang):
    """
    Validate languages based on settings
    """
    if lang in [language[0] for language in settings.LANGUAGES]:
        return lang
    return 'en'
