"""
Units views
"""

import datetime

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .models import UnitSystem, UnitNotFound
from geocurrency.core.helpers import validate_language


class ListFragment(View):
    """
    Fragment template for turbo frame
    """

    def _controller(self, request: HttpRequest, data: dict, *args, **kwargs):
        """
        Handle request
        :param request: HttpRequest
        :param data: dict from request
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        unit_system = UnitSystem(system_name='SI', fmt_locale=language)
        try:
            unit = unit_system.unit(data.get('unit', 'meter'))
        except UnitNotFound:
            unit = None
        try:
            dest_unit = unit_system.unit(data.get('dest_unit', 'kilometer'))
        except UnitNotFound:
            dest_unit = None
        units = [unit_system.unit(u) for u in unit_system.available_unit_names()]
        dest_units = [unit_system.unit(str(u)) for u in unit_system.ureg.get_compatible_units(
            input_units=unit.code)]
        try:
            value = float(data.get('value', 10))
        except ValueError:
            value = 0
        q_ = unit_system.ureg.Quantity
        result = q_(value, unit.code).to(dest_unit.code)
        return render(
            request,
            'frame.html',
            context={
                'dom_id': 'units',
                'model_template': 'units/partial/list.html',
                'units': units,
                'unit': unit,
                'dest_unit': dest_unit,
                'dest_units': dest_units,
                'value': value,
                'result': f'{result}',
                'timestamp': datetime.datetime.now().timestamp()
            }
        )

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Handle GET request
        :param request: HttpRequest
        """
        return self._controller(
            request=request,
            data=request.GET,
            *args,
            **kwargs
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Handle POST request
        :param request: HttpRequest
        """
        return self._controller(
            request=request,
            data=request.POST,
            *args,
            **kwargs
        )
