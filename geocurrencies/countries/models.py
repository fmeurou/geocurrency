import os

import pytz
import re
import requests
from datetime import datetime
from django.conf import settings
from django.db import models
from pytz import timezone

from .helpers import ColorProximity, hextorgb
from .settings import *


class CountryManager(models.Manager):

    def get_by_color(self, color, proximity=0.1):
        """
        Take a hex color and finds near country based on flag and color proximity
        :param color: hex color (FFF, FFFFFF, FFFFFFFF, #FFF, #FFFFFF, #FFFFFFFF)
        :param proximity: succes rate, positive if below (100 is opposite, 0 is identical
        """
        cp = ColorProximity()
        rgb_color = hextorgb(color)
        countries = []
        for country in Country.objects.filter(colors__isnull=False):
            for fc in country.colors.split(','):
                flag_color = hextorgb(fc)
                if cp.proximity(rgb_color, flag_color) < proximity:
                    countries.append(country.pk)
                    break
        return Country.objects.filter(pk__in=set(countries))


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
    colors = models.CharField(max_length=2000, null=True)
    objects = CountryManager()

    @property
    def timezones(self):
        output = []
        fmt = '%z'
        base_time = datetime.utcnow()
        for tz_info in pytz.country_timezones[self.alpha_2]:
            tz = timezone(tz_info)
            offset = tz.localize(base_time).strftime(fmt)
            numeric_offset = float(offset[:-2] + '.' + offset[-2:])
            output.append({
                'name': tz_info,
                'offset': f'UTC {offset}',
                'numeric_offset': numeric_offset,
                'current_time': base_time.astimezone(tz).strftime('%Y-%m-%d %H:%M')
            })
        return sorted(output, key=lambda x: x['numeric_offset'])

    def download_flag(self):
        flag_path = os.path.join(settings.MEDIA_ROOT, self.alpha_2 + '.svg')
        if not os.path.exists(flag_path):
            response = requests.get(FLAG_SOURCE.format(alpha_2=self.alpha_2))
            try:
                flag_content = response.text
                flag_file = open(flag_path, 'w')
                flag_file.write(flag_content)
                flag_file.close()
            except IOError:
                print("enable to write file", flag_path)

    def analyze_flag(self):
        flag_path = os.path.join(settings.MEDIA_ROOT, self.alpha_2 + '.svg')
        with open(flag_path, 'r') as flag:
            content = flag.read()
            result = re.findall(r'\#[0-9A-Fa-f]{1,2}[0-9A-Fa-f]{1,2}[0-9A-Fa-f]{1,2}', content)
            if result:
                self.colors = ','.join(result)
                self.save()


class Subdivision(models.Model):
    country = models.ForeignKey(Country, related_name='subdivisions', on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    code = models.CharField(max_length=6)
    type = models.CharField(max_length=255)
