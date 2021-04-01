"""
Currencies views
"""

import logging
import os
import datetime

import requests
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from sendfile import sendfile

from .models import Currency


class TurboCurrencyListView(View):

    def get(self, request, *args, **kwargs):
        currencies = Currency.search(term=request.GET.get('search', ''))
        return render(
            request,
            'currencies/partial/list.html',
            context={
                'currencies': currencies,
                'timestamp': datetime.datetime.now().timestamp()
            }
        )