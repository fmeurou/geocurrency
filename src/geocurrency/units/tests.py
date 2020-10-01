import uuid

import pint
from django.core.cache import cache
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.test import APIClient

from .models import UnitSystem, UnitConverter
from .serializers import UnitAmountSerializer


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

    def test_list_with_dimension_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'family': 'length'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set([c['family'] for c in response.json()]), {'length'})

    def test_list_with_dimension_2_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'family': 'surface'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set([c['family'] for c in response.json()]), {'surface'})

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_compatible_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/compatible/'
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
        self.assertIn('SI', [us['system_name'] for us in response.json()])

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get(
            '/units/SI/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("system_name"), "SI")
        self.assertIn("length", response.json().get("dimensions"))

    def test_retrieve_request_not_found(self):
        client = APIClient()
        response = client.get(
            '/units/sO/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UnitConverterTest(TestCase):
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        self.converter = UnitConverter(base_system='SI', base_unit='meter')
        self.amounts = [
            {
                'system': 'SI',
                'unit': 'furlong',
                'value': 1,
                'date_obj': '2020-07-22'
            },
            {
                'system': 'SI',
                'unit': 'yard',
                'value': 1,
                'date_obj': '2020-07-22'
            },
        ]
        self.trash_amounts = [
            {
                'system': 'si',
                'unit': 'trop',
                'value': 100,
                'date_obj': '01/01/2020'
            },
            {
                'system': 'SI',
                'unit': 'trop',
                'value': 2,
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 'tete',
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 0,
                'date_obj': '01/01/2021'
            },
        ]

    def test_created(self):
        self.assertEqual(self.converter.status, self.converter.INITIATED_STATUS)

    def test_add_data(self):
        errors = self.converter.add_data(self.amounts)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status, self.converter.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_amounts(self):
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(self.trash_amounts)
        self.assertEqual(len(errors), 3)
        self.assertIn("system", errors[0])
        self.assertIn("value", errors[1])
        self.assertIn("date_obj", errors[2])

    def test_add_empty_data(self):
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(data=None)
        self.assertEqual(len(errors), 1)

    def test_convert(self):
        result = self.converter.convert()
        self.assertEqual(result.id, self.converter.id)
        self.assertEqual(result.target, 'meter')
        self.assertEqual(self.converter.status, self.converter.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)

    def test_convert_request(self):
        amounts = UnitAmountSerializer(self.amounts, many=True)
        client = APIClient()
        response = client.post(
            '/units/convert/',
            data={
                'data': amounts.data,
                'base_system': 'SI',
                'base_unit': 'meter'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sum', response.json())
        self.assertEqual(len(response.json().get('detail')), len(self.amounts))

    def test_convert_batch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        amounts = UnitAmountSerializer(self.amounts, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': amounts.data,
                'base_system': 'SI',
                'base_unit': 'meter',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.post(
            '/units/convert/',
            data={
                'data': amounts.data,
                'batch_id': batch_id,
                'base_system': 'SI',
                'base_unit': 'meter',
                'eob': True
            },
            format='json')
        self.assertEqual(response.json().get('status'), UnitConverter.FINISHED)
        self.assertEqual(len(response.json().get('detail')), 2 * len(self.amounts))

    def test_watch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        amounts = UnitAmountSerializer(self.amounts, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': amounts.data,
                'base_system': 'SI',
                'base_unit': 'meter',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.get(
            f'/watch/{str(batch_id)}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'), UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
