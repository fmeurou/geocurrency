import pint
from datetime import datetime
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from rest_framework.test import APIClient
from rest_framework import status

from .models import UnitSystem, Unit


class UnitTest(TestCase):

    def test_creation(self):
        us = UnitSystem()
        unit = us.unit('meter')
        self.assertTrue(isinstance(unit.unit, pint.Unit))

    def test_readable_dimension(self):
        us = UnitSystem()
        unit = us.unit(unit_name='meter')
        self.assertEqual(unit.readable_dimension, _('length'))
        unit = us.unit(unit_name='US_international_ohm')
        self.assertEqual(unit.readable_dimension, f"{_('length')}^2 * {_('mass')} / {_('current')}^2 / {_('time')}^3")

    def test_list_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UnitSystemTest(TestCase):

    def test_available_systems(self):
        us = UnitSystem()
        available_systems = us.available_systems()
        self.assertEqual(available_systems, ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks'])

    def test_available_units(self):
        us = UnitSystem(system_name='imperial')
        available_units = us.available_unit_names()
        self.assertIn('UK_hundredweight', available_units)

    def test_available_units_different(self):
        us = UnitSystem(system_name='mks')
        available_units = us.available_unit_names()
        self.assertIn('meter', available_units)
        self.assertNotIn('UK_hundredweight', available_units)
        imperial = UnitSystem(system_name='imperial')
        imperial_available_units = imperial.available_unit_names()
        self.assertIn('UK_hundredweight', imperial_available_units)

    def test_units_per_dimensionality(self):
        us = UnitSystem(system_name='mks')
        upd = us.units_per_dimensionality()
        self.assertIn(_('length'), upd)

    def test_dimensionalities(self):
        us = UnitSystem(system_name='mks')
        dims = us.dimensionalities
        self.assertIn(_('length'), dims)

    def test_list_request(self):
        client = APIClient()
        response = client.get(
            '/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get(
            '/units/SI/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_request_not_found(self):
        client = APIClient()
        response = client.get(
            '/units/si/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)