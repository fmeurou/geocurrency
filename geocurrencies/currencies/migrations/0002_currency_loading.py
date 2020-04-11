import csv
import os

from django.db import migrations

import geocurrencies


def load_data(apps, schema_editor):
    CurrencyModel = apps.get_model('currencies', 'CurrencyModel')
    CurrencyCountry = apps.get_model('currencies', 'CurrencyCountry')
    Country = apps.get_model('countries', 'Country')
    data_path = os.path.join(os.path.dirname(os.path.abspath(geocurrencies.__file__)), 'data', 'data.csv')
    with open(data_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                numeric = int(row['ISO4217_Currency_Numeric_Code'])
            except ValueError:
                numeric = 0
            try:
                exponent = int(row['ISO4217_Currency_Minor_Unit'])
            except ValueError:
                exponent = 0
            print(
                numeric,
                row['ISO4217_Currency_Alphabetic_Code'],
                row['ISO4217_Currency_Name'],
                exponent
            )
            if row['ISO4217_Currency_Alphabetic_Code']:
                currency, created = CurrencyModel.objects.get_or_create(
                    numeric=numeric,
                    code=row['ISO4217_Currency_Alphabetic_Code'],
                    name=row['ISO4217_Currency_Name'],
                    exponent=exponent
                )
                try:
                    country = Country.objects.get(alpha_3=row['ISO3166_1_Alpha_3'])

                    CurrencyCountry.objects.create(
                        currency=currency,
                        country=country
                    )
                except Country.DoesNotExist:
                    print("invalid country code", row['ISO3166_1_Alpha_3'])


class Migration(migrations.Migration):
    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
