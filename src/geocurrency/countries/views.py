"""
Country views
"""

import datetime
import logging
import os

import requests
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from sendfile import sendfile

from .models import Country, CountryNotFoundError
from .settings import *


class FlagView(View):
    """
    Try to get flag image from MEDIA_ROOT cache or download it from FLAG_SOURCE
    """

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk, *args, **kwargs):
        try:
            country = Country(alpha_2=pk)
            flag_path = os.path.join(settings.MEDIA_ROOT, country.alpha_2 + '.svg')
            if not os.path.exists(flag_path):
                response = requests.get(FLAG_SOURCE.format(alpha_2=country.alpha_2))
                try:
                    flag_content = response.text
                    flag_file = open(flag_path, 'w')
                    flag_file.write(flag_content)
                    flag_file.close()
                except IOError:
                    logging.error("unable to write file", flag_path)
                    return HttpResponseBadRequest("Error fetching file")
            return sendfile(request, flag_path)
        except CountryNotFoundError as e:
            logging.error("Error fetching country")
            logging.error(e)
            return HttpResponseNotFound("Invalid country")


class TurboCountryListView(View):

    def get(self, request, *args, **kwargs):
        countries = Country.search(term=request.GET.get('search', ''))
        return render(
            request,
            'country/partial/list.html',
            context={
                'countries': countries,
                'timestamp': datetime.datetime.now().timestamp()
            }
        )
