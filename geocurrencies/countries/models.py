import pytz
from django.db import models
from pytz import timezone
from datetime import datetime


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)
    formal_name = models.CharField(max_length=2000)
    capital = models.CharField(max_length=255)
    continent = models.CharField(max_length=2)
    dial = models.CharField(max_length=20)
    region = models.CharField(max_length=255)
    subregion = models.CharField(max_length=255)
    dependency = models.CharField(max_length=255)

    @property
    def timezones(self):
        output = []
        fmt = '%z'
        base_time = datetime(year=2020, month=1, day=1)
        for tz_info in pytz.country_timezones[self.alpha_2]:
            tz = timezone(tz_info)
            offset = tz.localize(base_time).strftime(fmt)
            numeric_offset = float(offset[:-2] + '.' + offset[-2:])
            output.append({
                'name': tz_info,
                'offset': f'UTC {offset}',
                'numeric_offset': numeric_offset
            })
        return sorted(output, key=lambda x:x['numeric_offset'])


class Subdivision(models.Model):
    country = models.ForeignKey(Country, related_name='subdivisions', on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    code = models.CharField(max_length=6)
    type = models.CharField(max_length=255)
