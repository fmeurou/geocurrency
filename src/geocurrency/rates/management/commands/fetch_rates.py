from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fetch rates for a date'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='*', type=str)

    def handle(self, *args, **options):
        from geocurrency.currencies.models import Currency
        from geocurrency.rates.models import Rate

        for currency in Currency.all_currencies():
            self.stdout.write('fetching rates for currency {}.'.format(currency.code))
            Rate.objects.fetch_rates(base_currency=currency.code)
