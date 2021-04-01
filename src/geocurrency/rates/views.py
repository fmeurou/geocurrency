"""
Rates views
"""

import datetime

from django.shortcuts import render
from django.views import View

from geocurrency.currencies.models import Currency
from .models import Rate


class TurboRateListView(View):

    def get(self, request, *args, **kwargs):
        from_currency = request.GET.get('from_currency', 'USD')
        to_currency = request.GET.get('to_currency', 'EUR')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
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
            'rates/partial/list.html',
            context={
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
