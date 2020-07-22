import logging
from django.apps import AppConfig, apps
from django.conf import settings


class CountryConfig(AppConfig):
    name = 'countries'
    verbose_name = "Countries query app"

    def ready(self):
        super(CountryConfig, self).ready()



