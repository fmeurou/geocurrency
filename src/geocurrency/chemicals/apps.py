"""
Chemicals Django application
"""
from django.apps import AppConfig


class ChemicalsConfig(AppConfig):
    """
    CountryConfig class
    """
    name = 'geocurrency.chemicals'
    verbose_name = "Chemicals query app"

    def ready(self):
        """
        Setup config
        """
        super(ChemicalsConfig, self).ready()
