from django.db import migrations
from iso4217 import Currency
from geocurrencies.currencies.tasks import import_history_rates


def load_data(apps, schema_editor):
    import_history_rates()


class Migration(migrations.Migration):
    dependencies = [
        ('currencies', '0002_currency_loading'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
