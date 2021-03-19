"""
Countries Django application
"""
from django.apps import AppConfig


class CountryConfig(AppConfig):
    """
    CountryConfig class
    """
    name = 'countries'
    verbose_name = "Countries query app"

    def ready(self):
        """
        Setup config
        """
        super(CountryConfig, self).ready()
