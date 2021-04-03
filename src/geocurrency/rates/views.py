"""
Rates views
"""

import datetime

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from geocurrency.currencies.models import Currency
from .models import Rate


class TurboRateListView(View):
    """
    View used for turbo-frames
    """

    def _controller(self, request: HttpRequest, data: dict, *args, **kwargs):
        """
        handle request
        :param request: Request
        :param data: dict from request GET or POST
        """
        from_currency = data.get('from_currency', 'USD')
        to_currency = data.get('to_currency', 'EUR')
        from_date = data.get('from_date', '')
        to_date = data.get('to_date', '')
        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        else:
            from_date = datetime.date.today() - datetime.timedelta(7)
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        else:
            to_date = datetime.date.today()
        return render(
            request,
            'frame.html',
            context={
                'dom_id': 'rates',
                'model_template': 'rates/partial/list.html',
                'currencies': Currency.all_currencies(),
                'from_date': from_date,
                'to_date': to_date,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rates': Rate.objects.filter(
                    currency=from_currency,
                    base_currency=to_currency,
                    value_date__gte=from_date,
                    value_date__lte=to_date
                ),
                'timestamp': datetime.datetime.now().timestamp()
            }
        )

    def get(self, request, *args, **kwargs):
        """
        Handle GET request
        """
        return self._controller(request=request, data=request.GET, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request
        """
        return self._controller(
            request=request,
            data=request.POST,
            *args,
            **kwargs
        )
