"""
Currencies views
"""

import datetime

from django.shortcuts import render
from django.views import View

from .models import Currency


class TurboCurrencyListView(View):
    """
    List fragment for turbo frame
    """

    def get(self, request, *args, **kwargs):
        """
        Get a list of currencies
        """
        currencies = Currency.search(term=request.GET.get('search', ''))
        return render(
            request,
            'frame.html',
            context={
                'dom_id': 'currencies',
                'model_template': 'currencies/partial/list.html',
                'currencies': currencies,
                'timestamp': datetime.datetime.now().timestamp()
            }
        )
