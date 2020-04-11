import csv
import os

from django.db import migrations

import geocurrencies


def load_data(apps, schema_editor):
    Country = apps.get_model('countries', 'Country')
    data_path = os.path.join(os.path.dirname(os.path.abspath(geocurrencies.__file__)), 'data', 'data.csv')
    with open(data_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                Country.objects.create(
                    id=int(row['ISO3166_1_Numeric_Code']),
                    name=row['Official_Name_English'],
                    alpha_2=row['ISO3166_1_Alpha_2'],
                    alpha_3=row['ISO3166_1_Alpha_3'],
                    formal_name=row['UN_Term_English_Formal'],
                    capital=row['Capital'],
                    continent=row['Continent'],
                    dial=row['Dial'],
                    region=row['Region_Name'],
                    subregion=row['Sub_Region_Name'],
                    dependency=row['Is_Independent'] if row['Is_Independent'] != 'Yes' else ''
                )
            except ValueError:
                print("invalid numeric id", row['Official_Name_English'])


class Migration(migrations.Migration):
    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
