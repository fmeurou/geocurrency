import pint
from datetime import datetime
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from .models import UnitSystem, Unit


class UnitTest(TestCase):

    def test_creation(self):
        unit = Unit('meter')
        self.assertTrue(isinstance(unit.unit, pint.Unit))

    def test_readable_dimension(self):
        unit = Unit('meter')
        self.assertEqual(unit.readable_dimension, _('length'))
        unit = Unit('US_international_ohm')
        self.assertEqual(unit.readable_dimension, f"{_('length')}^2 * {_('mass')} / {_('current')}^2 / {_('time')}^3")


class UnitSystemTest(TestCase):

    def test_available_systems(self):
        print(datetime.now())
        us = UnitSystem()
        available_systems = us.available_systems()
        print("available systems", datetime.now())
        self.assertEqual(available_systems, ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks'])

    def test_available_units(self):
        print(datetime.now())
        us = UnitSystem(system='imperial')
        available_units = us.available_units()
        print("available units", datetime.now())
        self.assertIn('UK_hundredweight', available_units)

    def test_available_units_different(self):
        print("available_units end", datetime.now())
        us = UnitSystem(system='mks')
        available_units = us.available_units()
        print("available_units si", datetime.now())
        self.assertIn('meter', available_units)
        self.assertNotIn('UK_hundredweight', available_units)
        imperial_available_units = us.available_units('imperial')
        print("available_units imperial", datetime.now())
        self.assertIn('UK_hundredweight', imperial_available_units)

    def test_units_per_dimensionality(self):
        print(datetime.now())
        us = UnitSystem(system='mks')
        upd = us.units_per_dimensionality()
        print("units_per_dimensionality", datetime.now())
        self.assertIn(_('length'), upd)

    def test_dimensionalities(self):
        print(datetime.now())
        us = UnitSystem(system='mks')
        dims = us.dimensionalities
        print("end dims", datetime.now())
        self.assertIn(_('length'), dims)
