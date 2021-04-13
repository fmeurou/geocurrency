"""
Command to fetch rates for all currencies
"""
from datetime import datetime, date

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
        parser.add_argument("-f", '--from_date', type=str,
                            help="Date in YYYY-MM-DD format."
                                 "Start fetching from this date, defaults to today")
        parser.add_argument("-t", '--to_date', type=str,
                            help="Date in YYYY-MM-DD format."
                                 "End of fetch range. defaults to today")
        parser.add_argument("-s", '--service', type=str,
                            help="Rate service name. (forex, currencylayer, or other)"
                                 "Defaults to forex. See SERVICES in settings")

    def handle(self, *args, **options):
        """
        Handle call
        """
        from geocurrency.currencies.models import Currency
        from geocurrency.rates.models import Rate
        today = date.today().strftime('%Y-%m-%d')
        try:
            from_date = datetime.strptime(options.get('from_date') or today, '%Y-%m-%d')
            to_date = datetime.strptime(options.get('to_date') or today, '%Y-%m-%d')
        except ValueError:
            print("invalid dates")
            exit(-1)
        rate_service = options.get('service') or 'forex'

        for currency in Currency.all_currencies():
            self.stdout.write('fetching rates for currency {}.'.format(currency.code))
            Rate.objects.fetch_rates(
                base_currency=currency.code,
                date_obj=from_date,
                to_obj=to_date,
                rate_service=rate_service
            )
