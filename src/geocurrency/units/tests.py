"""
Units tests
"""
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
from .exceptions import UnitSystemNotFound, UnitDuplicateError, UnitDimensionError, UnitValueError
from .models import UnitSystem, UnitConverter, Dimension, DimensionNotFound, CustomUnit, \
    ExpressionCalculator, Operand
from .serializers import QuantitySerializer, ExpressionSerializer


class DimensionTest(TestCase):
    """
    Test Dimension object
    """

    def setUp(self):
        """
        Setup test environment
        """
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
        """
        Test creation of a dimension
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        self.assertTrue(isinstance(dimension, Dimension))

    def test_bad_creation(self):
        """
        Test creation with wrong parameters
        """
        us = UnitSystem()
        self.assertRaises(DimensionNotFound, Dimension, unit_system=us, code='length')

    def test_dimension_units(self):
        """
        Test listing dimension units
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit_codes = [unit.code for unit in dimension.units()]
        self.assertIn('meter', unit_codes)

    def test_compounded_dimension_units(self):
        """
        Test units list for [compounded] special dimension
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[compounded]')
        unit_codes = [unit.code for unit in dimension.units()]
        self.assertIn('number_english', unit_codes)

    def test_custom_dimension_superuser_units(self):
        """
        Test units list for [custom] special dimension for superuser
        """
        us = UnitSystem(user=self.admin)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.admin)), 2)

    def test_custom_dimension_superuser_key_units(self):
        """
        Test units list for [custom] dimension with superuser rights with a key
        """
        us = UnitSystem(user=self.admin, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.admin, key=self.key)), 1)

    def test_custom_dimension_user_units(self):
        """
        Test units list for a user
        """
        us = UnitSystem(user=self.user)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.user)), 2)

    def test_custom_dimension_user_key_units(self):
        """
        Test units list for a user with a key
        """
        us = UnitSystem(user=self.user, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units(user=self.user, key=self.key)), 1)

    def test_custom_dimension_no_user_units(self):
        """
        Test units list if no user
        """
        us = UnitSystem(user=self.user)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units()), 0)


class UnitTest(TestCase):
    """
    Test Unit object
    """

    def test_creation(self):
        """
        Test creation of Unit
        """
        us = UnitSystem()
        unit = us.unit('meter')
        self.assertTrue(isinstance(unit.unit, pint.Unit))

    def test_dimensions(self):
        """
        Test unit dimensions
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit = us.unit('meter')
        self.assertIn(dimension.code, [d.code for d in unit.dimensions])

    def test_readable_dimension(self):
        """
        Test user readable dimension for unit
        """
        us = UnitSystem()
        unit = us.unit(unit_name='meter')
        self.assertEqual(unit.readable_dimension, _('length'))
        unit = us.unit(unit_name='US_international_ohm')
        self.assertEqual(unit.readable_dimension,
                         f"{_('length')}^2 * {_('mass')} / {_('current')}^2 / {_('time')}^3")


class UnitAPITest(TestCase):
    """
    Test Unit APIs
    """

    def test_list_request(self):
        """
        Test list of units
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sorted_list_request(self):
        """
        Test list with ordering
        """
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
        """
        Test requireng a translated list
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'fr'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bad_language_request(self):
        """
        Test requiring an invalid translation
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'theta'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_per_dimension_request(self):
        """
        Test list of units grouped by dimension
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_list_per_dimension_request(self):
        """
        Test list of units with invalid unit system
        """
        client = APIClient()
        response = client.get(
            '/units/hello/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_bad_dimension_request(self):
        """
        Test  units list with invalid dimension filter
        """
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
        """
        Test list filtered by dimension
        """
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
        """
        Test list of [compounded dimension]
        """
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
        """
        Test another dimension
        """
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
        """
        Test retrieve unit
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request(self):
        """
        Test retrieve invalid unit
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/plouf/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_compatible_request(self):
        """
        Test list compatible units
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/compatible/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UnitSystemTest(TestCase):
    """
    UnitSystem tests
    """

    def setUp(self):
        """
        Setup test environment
        """
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
        """
        tear down environment
        """
        settings.GEOCURRENCY_ADDITIONAL_UNITS = self.old_setting

    def test_available_systems(self):
        """
        Test list of available unit systems
        """
        us = UnitSystem()
        available_systems = us.available_systems()
        self.assertEqual(available_systems,
                         ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks'])

    def test_available_units(self):
        """
        Test list of avaible units
        """
        us = UnitSystem(system_name='imperial')
        available_units = us.available_unit_names()
        self.assertIn('UK_hundredweight', available_units)

    def test_available_base_units(self):
        """
        Test list of availbale base units
        """
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('kilogram', available_units)

    def test_available_additional_units(self):
        """
        Test list of available additional units
        """
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('my_unit', available_units)

    def test_test_additional_base_units(self):
        """
        test add base units test
        """
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(ADDITIONAL_BASE_UNITS)
        self.assertTrue(available_units)

    def test_test_additional_units(self):
        """
        Test additionnal units addition test
        """
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(settings.GEOCURRENCY_ADDITIONAL_UNITS)
        self.assertFalse(available_units)

    def test_available_units_different(self):
        """
        Test avaible available unitsfor another unit system
        """
        us = UnitSystem(system_name='mks')
        available_units = us.available_unit_names()
        self.assertIn('meter', available_units)
        self.assertNotIn('UK_hundredweight', available_units)
        imperial = UnitSystem(system_name='imperial')
        imperial_available_units = imperial.available_unit_names()
        self.assertIn('UK_hundredweight', imperial_available_units)

    def test_units_per_dimensionality(self):
        """
        Test listing units per dimensionality
        """
        us = UnitSystem(system_name='mks')
        upd = us.units_per_dimensionality()
        self.assertIn(_('length'), upd)

    def test_dimensionalities(self):
        """
        Test dimensionalities of a unit system
        """
        us = UnitSystem(system_name='mks')
        dims = us.dimensionalities
        self.assertIn(_('length'), dims)


class UnitSystemAPITest(TestCase):
    """
    UnitSystem API tests
    """

    def setUp(self):
        """
        Setup test environment
        """
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

    def test_list_request(self):
        """
        Test unit system list API
        """
        client = APIClient()
        response = client.get(
            '/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('SI', [us['system_name'] for us in response.json()])

    def test_retrieve_request(self):
        """
        Test retrieve unit system API
        """
        client = APIClient()
        response = client.get(
            '/units/SI/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("system_name"), "SI")

    def test_list_dimensions_request(self):
        """
        Test dimensions list request
        """
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("[length]", [r['code'] for r in response.json()])

    def test_list_sorted_dimensions_request(self):
        """
        Test sorted dimensions request
        """
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
        """
        Test invalid retrieve request
        """
        client = APIClient()
        response = client.get(
            '/units/sO/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UnitConverterTest(TestCase):
    """
    Test UnitConverter object
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
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
        """
        Test converter  creation
        """
        self.assertEqual(self.converter.status, self.converter.INITIATED_STATUS)

    def test_add_data(self):
        """
        Test adding data to a converter
        """
        errors = self.converter.add_data(self.quantities)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status, self.converter.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_quantities(self):
        """
        Test adding trash to a converter
        """
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(self.trash_quantities)
        self.assertEqual(len(errors), 3)
        self.assertIn("system", errors[0])
        self.assertIn("value", errors[1])
        self.assertIn("date_obj", errors[2])

    def test_add_empty_data(self):
        """
        Test adding empty values to a converter
        """
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(data=None)
        self.assertEqual(len(errors), 1)

    def test_convert(self):
        """
        Test conversion
        """
        result = self.converter.convert()
        self.assertEqual(result.id, self.converter.id)
        self.assertEqual(result.target, 'meter')
        self.assertEqual(self.converter.status, self.converter.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)


class UnitConverterAPITest(TestCase):
    """
    Test UnitConverter API object
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
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

    def test_convert_request(self):
        """
        Test conversion API
        """
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
        """
        Test batch conversion
        """
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
        """
        Test observation of a batch
        """
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
    """
    CustomUnit tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_creation(self):
        """
        Test creation of a CustomUnit
        """
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

    def test_creation_with_dash(self):
        """
        Test creation of a CustomUnit with - in code, symbol and alias
        """
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my-unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="m-yu",
            alias="m-yu")
        self.assertEqual(cu.user, self.user)
        self.assertEqual(cu.key, self.key)
        self.assertEqual(cu.unit_system, 'SI')
        self.assertEqual(cu.code, 'my_unit')
        self.assertEqual(cu.name, 'My Unit')
        self.assertEqual(cu.relation, '1.5 meter')
        self.assertEqual(cu.symbol, 'm_yu')
        self.assertEqual(cu.alias, 'm_yu')
        self.assertEqual(
            CustomUnit.objects.filter(user=self.user, key=self.key, unit_system='SI',
                                      code='my_unit').count(),
            1)

    def test_invalid_creation_params(self):
        """
        Test invalid creation params
        """
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
        """
        Test duplicated unit
        """
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

    def test_inception_unit_params(self):
        """
        Test duplicated unit
        """
        self.assertRaises(
            UnitValueError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='inception',
            name='My Inception',
            relation="1.5 inception",
            symbol="inc",
            alias="inc"
        )

    def test_wrong_dimensionality_unit_params(self):
        """
        Test unit creation with wrong dimensionality
        """
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


class CustomUnitTestAPI(TestCase):
    """
    CustomUnit API tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_list_request(self):
        """
        Test list of custom units
        """
        client = APIClient()
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_connected_list_request(self):
        """
        Test list of custom units with connected user
        """
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

    def test_connected_duplicate_post(self):
        """
        Test list of custom units with connected user
        """
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
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_409_CONFLICT)

    def test_connected_unit_system_request(self):
        """
        Test list of custom units with connected user
        """
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
        response = client.get(
            '/units/mks/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 0)
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 0)

    def test_connected_list_key_request(self):
        """
        Test list of custom units with connected user and a key
        """
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
        """
        Test list of units with custom unit and connected user
        """
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
        """
        Another test of a list of units with a custom unit
        """
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
        """
        Test key isolation
        """
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
        """
        Another isolation test
        """
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
    """
    Test Expression
    """

    def setUp(self):
        """
        Setup test environment
        """
        self.us = UnitSystem(system_name='SI')

    def tearDown(self):
        """
        tear down environment
        """
        self.us = None

    def test_valid_serializer_payload(self):
        """
        Test serializer validation
        """
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
        """
        Test invalid payload
        """
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
        """
        Test Quantity coherency
        """
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
        """
        Test wrong parameters
        """
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
        """
        Test empty expression in payload
        """
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

    def test_empty_serializer_operands(self):
        """
        Test empty operands list in payload
        """
        payload = {
            'expression': '(3*{a}+15*{b})-c',
            'operands': []
        }
        es = ExpressionSerializer(data=payload)
        self.assertFalse(es.is_valid(unit_system=self.us))

    def test_formula_validation_request(self):
        """
        Test formula syntax validation
        """
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


class OperandTest(TestCase):
    """
    Test Operand
    """

    def setUp(self):
        self.us = UnitSystem(system_name='SI')

    def test_validate(self):
        op = Operand(
            name='test',
            value=0,
            unit='m/s'
        )
        self.assertTrue(op.validate())
        op = Operand(
            name='',
            value=1,
            unit='m/s'
        )
        self.assertFalse(op.validate())
        op = Operand(
            name='test',
            value=None,
            unit='m/s'
        )
        self.assertFalse(op.validate())
        op = Operand(
            name='test',
            value='a',
            unit='m/s'
        )
        self.assertFalse(op.validate())

    def test_get_unit_units(self):
        op = Operand(
            name='toto',
            value=15,
            unit='m/s'
        )
        self.assertTrue(op.validate())
        self.assertEqual(op.get_unit(self.us), 'm/s')

    def test_get_unit_dimensions(self):
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]'
        )
        self.assertIsInstance(q_(1, op.get_unit(self.us)), q_)

    def test_get_unit_mixed(self):
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]*L'
        )
        self.assertIsInstance(q_(1, op.get_unit(self.us)), q_)

    def test_get_unit_mixed_custom(self):
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]*L*plouf'
        )
        self.assertRaises(pint.errors.UndefinedUnitError, q_, 1, op.get_unit(self.us))


class ExpressionAPITest(TestCase):
    """
    Test Expression API
    """

    def setUp(self):
        """
        Setup test environment
        """
        self.us = UnitSystem(system_name='SI')

    def test_formula_validation_variable_exception_request(self):
        """
        Test formaula validation API
        """
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
        """
        Test wrong formula validation API
        """
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
    """
    Test expression calculator
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
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

    def tearDown(self):
        """
        tear down environment
        """
        self.unit_system = None

    def test_created(self):
        """
        Test calculator creation
        """
        self.assertEqual(self.calculator.status, self.calculator.INITIATED_STATUS)

    def test_add_data(self):
        """
        Test adding data to calculator
        """
        errors = self.calculator.add_data(self.expressions)
        self.assertEqual(errors, [])
        self.assertEqual(self.calculator.status, self.calculator.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.calculator.id))

    def test_trash_quantities(self):
        """
        Test adding trash to the calculator
        """
        calculator = ExpressionCalculator(unit_system='SI')
        self.assertEqual(len(calculator.add_data(self.trash_expressions)), 2)

    def test_add_empty_data(self):
        """
        Test adding empty data to the calculator
        """
        calculator = ExpressionCalculator(unit_system='SI')
        errors = calculator.add_data(data=None)
        self.assertEqual(len(errors), 1)

    def test_computation(self):
        """
        Test computation
        """
        result = self.calculator.convert()
        self.assertEqual(result.id, self.calculator.id)
        self.assertEqual(self.calculator.status, self.calculator.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.calculator.data))


class ExpressionCalculatorAPITest(TestCase):
    """
    Test expression calculator API
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
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

    def test_convert_request(self):
        """
        Test calculate API
        """
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
        """
        Test batch computation
        """
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
        """
        Test observation of the calculator
        """
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
        response = client.get(f'/watch/{str(batch_id)}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'), ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
