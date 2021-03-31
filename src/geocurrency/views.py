"""
Core views
"""
import datetime
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_safe
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .currencies.models import Currency
from .units.models import UnitSystem

@require_safe
def index(request):
    """
    Base page
    """

    return render(request, 'index.html', context={
        'currencies': Currency.all_currencies(ordering='name'),
        'unit_systems': UnitSystem.available_systems(),
        'cachebust': datetime.datetime.now().timestamp()
    })


@require_safe
def tos(request):
    """
    Term of Service view
    """
    return render(request, 'tos.html')


class LanguageView(APIView):
    """
    Language view
    """

    @action(['GET'], detail=False, url_path='languages', url_name="languages")
    def get(self, request, *args, **kwargs):
        """
        GET handler
        :param request: HTTPRequest
        """
        return Response(
            [{'name': language[1], 'code': language[0]} for language in settings.LANGUAGES],
            content_type="application/json")
