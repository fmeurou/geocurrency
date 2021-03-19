"""
Command to fetch rates for all currencies
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Fetch rates command
    """
    help = 'Fetch rates for a date'

    def add_arguments(self, parser):
        """
        Add date argument to the command
        """
        parser.add_argument('date', nargs='*', type=str)

    def handle(self, *args, **options):
        """
        Handle call
        """
        from geocurrency.currencies.models import Currency
        from geocurrency.rates.models import Rate

        for currency in Currency.all_currencies():
            self.stdout.write('fetching rates for currency {}.'.format(currency.code))
            Rate.objects.fetch_rates(base_currency=currency.code)
