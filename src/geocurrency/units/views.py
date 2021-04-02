"""
Units views
"""

import datetime

from django.shortcuts import render
from django.views import View

from .models import UnitSystem, UnitNotFound


class ListFragment(View):

    def get(self, request, *args, **kwargs):
        unit_system = UnitSystem(system_name='SI')
        try:
            unit = unit_system.unit(request.GET.get('unit', 'meter'))
        except UnitNotFound:
            unit = None
        try:
            dest_unit = unit_system.unit(request.GET.get('dest_unit', 'kilometer'))
        except UnitNotFound:
            dest_unit = None
        units = [unit_system.unit(u) for u in unit_system.available_unit_names()]
        try:
            value = float(request.GET.get('value', 10))
        except ValueError:
            value = 0
        q_ = unit_system.ureg.Quantity
        result = q_(value, unit.code).to(dest_unit.code)
        return render(
            request,
            'units/partial/list.html',
            context={
                'units': units,
                'unit': unit,
                'dest_unit': dest_unit,
                'value': value,
                'result': result,
                'timestamp': datetime.datetime.now().timestamp()
            }
        )
