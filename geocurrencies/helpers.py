import logging
from django.conf import settings


def service(apps, service_name: str, *args, **kwargs):
    service_path = settings.SERVICES[service_name]
    if not hasattr(apps, 'services'):
        setattr(apps, 'services', {})
    if service_name in apps.services:
        return apps.services.get(service_name)
    try:
        service = service_path.split('.')
        module_name = '.'.join(service[:-1])
        class_name = service[-1]
        module = __import__(module_name)
        service_class = getattr(module, class_name)
        service = service_class()
        apps.services[service_name] = service
    except (AttributeError, ImportError) as e:
        logging.error(e)
        return None