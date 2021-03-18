import json
import uuid

import pint
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from . import ADDITIONAL_BASE_UNITS
from .exceptions import UnitSystemNotFound, UnitDuplicateError, UnitDimensionError
from .models import UnitSystem, UnitConverter, Dimension, DimensionNotFound, CustomUnit, \
    ExpressionCalculator
from .serializers import QuantitySerializer, ExpressionSerializer


class DimensionTest(TestCase):

    def setUp(self):
        self.key = uuid.uuid4()
        self.admin = User.objects.create(
            username='admin',
            email='admin@local.dev',
            is_superuser=True
        )
        self.user = User.objects.create(
            username='test',
            email='test@local.dev'
        )
        CustomUnit.objects.create(
            user=self.user,
            unit_system='SI',
            code='user_unit',
            name='User Unit',
            relation="1.5 meter",
            symbol="uun",
            alias="uun"
        )
        CustomUnit.objects.create(
            user=self.user,
            unit_system='SI',
            key=self.key,
            code='user_key_unit',
            name='User Key Unit',
            relation="1.5 meter",
            symbol="ukun",
            alias="ukun"
        )

    def test_creation(self):
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        self.assertTrue(isinstance(dimension, Dimension))

    def test_bad_creation(self):
        us = UnitSystem()
        self.assertRaises(DimensionNotFound, Dimension, unit_system=us, code='length')

    def test_dimension_units(self):
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit_codes = [unit.code for unit in dimension.units()]
        self.assertIn('meter', unit_codes)

    def test_compounded_dimension_units(self):
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[compounded]')
        unit_codes = [unit.code for unit in dimension.units()]
        self.assertIn('number_english', unit_codes)

    def test_custom_dimension_superuser_units(self):
        us = UnitSystem(user=self.admin)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.admin)), 2)

    def test_custom_dimension_superuser_key_units(self):
        us = UnitSystem(user=self.admin, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.admin, key=self.key)), 1)

    def test_custom_dimension_user_units(self):
        us = UnitSystem(user=self.user)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.user)), 2)

    def test_custom_dimension_user_key_units(self):
        us = UnitSystem(user=self.user, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.user, key=self.key)), 1)

    def test_custom_dimension_no_user_units(self):
        us = UnitSystem(user=self.user)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units()), 0)


class UnitTest(TestCase):

    def test_creation(self):
        us = UnitSystem()
        unit = us.unit('meter')
        self.assertTrue(isinstance(unit.unit, pint.Unit))

    def test_dimensions(self):
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit = us.unit('meter')
        self.assertIn(dimension.code, [d.code for d in unit.dimensions])

    def test_readable_dimension(self):
        us = UnitSystem()
        unit = us.unit(unit_name='meter')
        self.assertEqual(unit.readable_dimension, _('length'))
        unit = us.unit(unit_name='US_international_ohm')
        self.assertEqual(unit.readable_dimension,
                         f"{_('length')}^2 * {_('mass')} / {_('current')}^2 / {_('time')}^3")

    def test_list_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sorted_list_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'ordering': 'code'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['code'], 'K_alpha_Cu_d_220')

    def test_list_language_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'fr'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bad_language_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'theta'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_per_dimension_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_list_per_dimension_request(self):
        client = APIClient()
        response = client.get(
            '/units/hello/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_bad_dimension_request(self):
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[hello]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_with_dimension_request(self):
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[length]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us, code='[length]').units()))

    def test_list_with_compounded_dimension_request(self):
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[compounded]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us, code='[compounded]').units()))

    def test_list_with_dimension_2_request(self):
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[area]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us, code='[area]').units()))

    def test_retrieve_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/plouf/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_compatible_request(self):
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/compatible/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UnitSystemTest(TestCase):

    def setUp(self):
        self.old_setting = getattr(settings, 'ADDITIONAL_UNITS', {})
        settings.GEOCURRENCY_ADDITIONAL_UNITS = {
            'SI': {
                'my_unit': {
                    'name': 'My Unit',
                    'symbol': 'my²',
                    'relation': '0.0001 meter / meter ** 2'
                },
                'bad_unit': {
                    'name': 'Bad unit',
                    'symbol': 'All hell loose',
                    'relation': 'My tailor is rich'
                }
            }
        }  # value tested against in the TestCase

    def tearDown(self):
        settings.GEOCURRENCY_ADDITIONAL_UNITS = self.old_setting

    def test_available_systems(self):
        us = UnitSystem()
        available_systems = us.available_systems()
        self.assertEqual(available_systems,
                         ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks'])

    def test_available_units(self):
        us = UnitSystem(system_name='imperial')
        available_units = us.available_unit_names()
        self.assertIn('UK_hundredweight', available_units)

    def test_available_base_units(self):
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('kilogram', available_units)

    def test_available_additional_units(self):
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('my_unit', available_units)

    def test_test_additional_base_units(self):
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(ADDITIONAL_BASE_UNITS)
        self.assertTrue(available_units)

    def test_test_additional_units(self):
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(settings.GEOCURRENCY_ADDITIONAL_UNITS)
        self.assertFalse(available_units)

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

    def test_list_dimensions_request(self):
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("[length]", [r['code'] for r in response.json()])

    def test_list_sorted_dimensions_request(self):
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/',
            data={
                'ordering': 'dimension'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("[length]", [r['code'] for r in response.json()])
        self.assertEqual(response.json()[0]['code'], '[wavenumber]')

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
        self.quantities = [
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
        self.trash_quantities = [
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
        errors = self.converter.add_data(self.quantities)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status, self.converter.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_quantities(self):
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(self.trash_quantities)
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
        quantities = QuantitySerializer(self.quantities, many=True)
        client = APIClient()
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
                'base_system': 'SI',
                'base_unit': 'meter'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sum', response.json())
        self.assertEqual(len(response.json().get('detail')), len(self.quantities))

    def test_convert_batch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        quantities = QuantitySerializer(self.quantities, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
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
                'data': quantities.data,
                'batch_id': batch_id,
                'base_system': 'SI',
                'base_unit': 'meter',
                'eob': True
            },
            format='json')
        self.assertEqual(response.json().get('status'), UnitConverter.FINISHED)
        self.assertEqual(len(response.json().get('detail')), 2 * len(self.quantities))

    def test_watch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        quantities = QuantitySerializer(self.quantities, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
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


class CustomUnitTest(TestCase):

    def setUp(self) -> None:
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_creation(self):
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my_unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu")
        self.assertEqual(cu.user, self.user)
        self.assertEqual(cu.key, self.key)
        self.assertEqual(cu.unit_system, 'SI')
        self.assertEqual(cu.code, 'my_unit')
        self.assertEqual(cu.name, 'My Unit')
        self.assertEqual(cu.relation, '1.5 meter')
        self.assertEqual(cu.symbol, 'myu')
        self.assertEqual(cu.alias, 'myu')
        self.assertEqual(
            CustomUnit.objects.filter(user=self.user, key=self.key, unit_system='SI',
                                      code='my_unit').count(),
            1)

    def test_invalid_creation_params(self):
        self.assertRaises(
            UnitSystemNotFound,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SO',
            code='my_unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu"
        )

    def test_duplicate_unit_params(self):
        self.assertRaises(
            UnitDuplicateError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='meter',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu"
        )

    def test_wrong_dimensionality_unit_params(self):
        self.assertRaises(
            UnitDimensionError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my_unit',
            name='My Unit',
            relation="1.5 brouzouf",
            symbol="myu",
            alias="myu"
        )

    def test_list_request(self):
        client = APIClient()
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_connected_list_request(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')

    def test_connected_list_key_request(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'key': self.key,
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu",
                'alias': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')

    def test_connected_unit_list_request(self):
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('ny_unit', [u['code'] for u in response.json()['results']])
        else:
            self.assertIn('ny_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_2_request(self):
        new_key = uuid.uuid4()
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        cu2 = CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('ny_unit', [u['code'] for u in response.json()['results']])
            self.assertIn('py_unit', [u['code'] for u in response.json()['results']])
        else:
            self.assertIn('ny_unit', [u['code'] for u in response.json()])
            self.assertIn('py_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_new_key_request(self):
        new_key = uuid.uuid4()
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        cu2 = CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
            data={
                'key': new_key
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('ny_unit', [u['code'] for u in response.json()])
        self.assertIn('py_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_self_key_request(self):
        new_key = uuid.uuid4()
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        cu2 = CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
            data={
                'key': self.key
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ny_unit', [u['code'] for u in response.json()])
        self.assertNotIn('py_unit', [u['code'] for u in response.json()])


class ExpressionTest(TestCase):

    def setUp(self):
        self.us = UnitSystem(system_name='SI')

    def test_valid_serializer_payload(self):
        payload = {
            'expression': '(3*{a}+15*{b})*6*{c}',
            'operands': [
                {
                    'name': 'a',
                    'value': 0.1,
                    'unit': 'kg'
                },
                {
                    'name': 'b',
                    'value': 15,
                    'unit': 'g'
                },
                {
                    'name': 'c',
                    'value': 12,
                    'unit': 's'
                }
            ]
        }
        es = ExpressionSerializer(data=payload)
        self.assertTrue(es.is_valid(unit_system=self.us))

    def test_invalid_serializer_expression(self):
        payload = {
            'expression': '(3*{a}+15*{b}) -',
            'operands': [
                {
                    'name': 'a',
                    'value': 0.1,
                    'unit': 'kg'
                },
                {
                    'name': 'b',
                    'value': 15,
                    'unit': 'g'
                },
                {
                    'name': 'c',
                    'value': 12,
                    'unit': 's'
                }
            ]
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_invalid_serializer_coherency(self):
        payload = {
            'expression': '(3*{a}+15*{b})-c',
            'operands': [
                {
                    'name': 'a',
                    'value': 0.1,
                    'unit': 'kg'
                },
                {
                    'name': 'b',
                    'value': 15,
                    'unit': 'g'
                },
                {
                    'name': 'c',
                    'value': 12,
                    'unit': 's'
                }
            ]
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_invalid_serializer_parameters(self):
        payload = {
            'expression': '(3*{a}+15*{b})-c',
            'operands': [
                {
                    'name': 'a',
                    'value': 0.1,
                    'unit': 'kg'
                },
                {
                    'name': 'b',
                    'value': 15,
                    'unit': 'g'
                }
            ]
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_empty_serializer_expression(self):
        payload = {
            'expression': '',
            'operands': [
                {
                    'name': 'a',
                    'value': 0.1,
                    'unit': 'kg'
                },
                {
                    'name': 'b',
                    'value': 15,
                    'unit': 'g'
                }
            ]
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_empty_serializer_variables(self):
        payload = {
            'expression': '(3*{a}+15*{b})-c',
            'operands': []
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_formula_validation_request(self):
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/validate/',
            data=json.dumps({
                'expression': "3*{a}+15*{b}",
                "operands": [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 15,
                        "unit": "g"
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_formula_validation_variable_exception_request(self):
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/validate/',
            data=json.dumps({
                'expression': "3*{a}+15*{b}",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_formula_validation_expression_exception_request(self):
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/validate/',
            data=json.dumps({
                'expression': "3*{a}+15*{b}+",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 15,
                        "unit": "g"
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class ExpressionCalculatorTest(TestCase):
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        self.calculator = ExpressionCalculator(unit_system='SI')
        self.unit_system = UnitSystem(system_name='SI')
        self.expressions = [
            {
                'expression': "3*{a}+15*{b}",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 15,
                        "unit": "g"
                    }
                ]
            },
            {
                'expression': "3*{a}+15*{b}+1000*{c}",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 150,
                        "unit": "g"
                    },
                    {
                        "name": "c",
                        "value": 250,
                        "unit": "mg"
                    },
                ]
            }
        ]
        self.trash_expressions = [
            {
                'expression': "3*{a}+15*{b}+",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 15,
                        "unit": "g"
                    }
                ]
            },
            {
                'expression': "3*{a}+15*{b}+1000*{c}",
                'operands': [
                    {
                        "name": "a",
                        "value": 0.1,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 150,
                        "unit": "g"
                    },
                    {
                        "name": "c",
                        "value": 250,
                        "unit": "s"
                    },
                ]
            }
        ]

    def test_created(self):
        self.assertEqual(self.calculator.status, self.calculator.INITIATED_STATUS)

    def test_add_data(self):
        errors = self.calculator.add_data(self.expressions)
        self.assertEqual(errors, [])
        self.assertEqual(self.calculator.status, self.calculator.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.calculator.id))

    def test_trash_quantities(self):
        calculator = ExpressionCalculator(unit_system='SI')
        self.assertEqual(len(calculator.add_data(self.trash_expressions)), 2)

    def test_add_empty_data(self):
        calculator = ExpressionCalculator(unit_system='SI')
        errors = calculator.add_data(data=None)
        self.assertEqual(len(errors), 1)

    def test_convert(self):
        result = self.calculator.convert()
        self.assertEqual(result.id, self.calculator.id)
        self.assertEqual(self.calculator.status, self.calculator.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.calculator.data))

    def test_convert_request(self):
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/calculate/',
            data={
                'data': self.expressions,
                'unit_system': 'SI',
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('detail')), len(self.expressions))
        self.assertEqual(response.json().get('detail')[0]['magnitude'], 0.525)

    def test_convert_batch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/calculate/',
            data={
                'data': self.expressions,
                'batch_id': batch_id,
                'unit_system': 'SI',

            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.post(
            '/units/SI/formulas/calculate/',
            data={
                'data': self.expressions,
                'unit_system': 'SI',
                'batch_id': batch_id,
                'eob': True
            },
            format='json')
        self.assertEqual(response.json().get('status'), ExpressionCalculator.FINISHED)
        self.assertEqual(len(response.json().get('detail')), 2 * len(self.expressions))

    def test_watch_request(self):
        batch_id = uuid.uuid4()
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/calculate/',
            data={
                'data': self.expressions,
                'batch_id': batch_id,
                'unit_system': 'SI',
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'), ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.get(
            f'/watch/{str(batch_id)}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'), ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
