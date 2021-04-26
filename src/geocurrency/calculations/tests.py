"""
Units tests
"""
import json
import uuid

import pint
from django.core.cache import cache
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from geocurrency.units.models import UnitSystem

from .models import ExpressionCalculator, Operand
from .serializers import ExpressionSerializer


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
        """
        Setup unit system
        """
        self.us = UnitSystem(system_name='SI')

    def test_validate(self):
        """
        Test operand validation
        """
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
        """
        Test units of operand
        """
        op = Operand(
            name='toto',
            value=15,
            unit='m/s'
        )
        self.assertTrue(op.validate())
        self.assertEqual(op.get_unit(self.us), 'm/s')

    def test_get_unit_uncertainty_and_magnitude(self):
        """
        Test uncertainty of operand
        """
        op = Operand(
            name='toto',
            value=15,
            unit='m/s',
            uncertainty="0.01"
        )
        self.assertTrue(op.validate())
        self.assertEqual(op.get_uncertainty(), 0.01)
        self.assertEqual(op.get_magnitude(), 15)

    def test_get_unit_uncertainty_percentage_and_magnitude(self):
        """
        Test uncertainty with a percentage
        """
        op = Operand(
            name='toto',
            value=15,
            unit='m/s',
            uncertainty="10%"
        )
        self.assertTrue(op.validate())
        self.assertEqual(op.get_uncertainty(), 15 * 0.1)
        self.assertEqual(op.get_magnitude(), 15)

    def test_get_unit_dimensions(self):
        """
        Test dimensions of units
        """
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]'
        )
        self.assertIsInstance(q_(1, op.get_unit(self.us)), q_)

    def test_get_unit_mixed(self):
        """
        Test operand with dimensions
        """
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]*L'
        )
        self.assertIsInstance(q_(1, op.get_unit(self.us)), q_)

    def test_get_unit_mixed_custom(self):
        """
        Test Operand with custom units
        """
        q_ = self.us.ureg.Quantity
        op = Operand(
            name='toto',
            value=15,
            unit='[mass]/[time]*L*plouf'
        )
        self.assertRaises(
            pint.errors.UndefinedUnitError,
            q_,
            1,
            op.get_unit(self.us)
        )


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
        self.expression_to_unit = [
            {
                'expression': "3*{a}+15*{b}",
                'operands': [
                    {
                        "name": "a",
                        "value": 200,
                        "unit": "kg"
                    },
                    {
                        "name": "b",
                        "value": 150000,
                        "unit": "g"
                    }
                ],
                'out_units': 'pound'
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
                        "value": 75,
                        "unit": "g"
                    },
                    {
                        "name": "c",
                        "value": 125,
                        "unit": "mg"
                    },
                ],
                'out_units': 'milligram'
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
                        "value": 75,
                        "unit": "g"
                    },
                    {
                        "name": "c",
                        "value": 125,
                        "unit": "mg"
                    },
                ],
                'out_units': 'L'
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
        self.assertEqual(
            self.calculator.status,
            self.calculator.INITIATED_STATUS)

    def test_add_data(self):
        """
        Test adding data to calculator
        """
        errors = self.calculator.add_data(self.expressions)
        self.assertEqual(errors, [])
        self.assertEqual(
            self.calculator.status,
            self.calculator.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.calculator.id))

    def test_trash_quantities(self):
        """
        Test adding trash to the calculator
        """
        calculator = ExpressionCalculator(unit_system='SI')
        errors = calculator.add_data(self.trash_expressions)
        self.assertEqual(len(errors), 3)
        self.assertEqual([list(c.keys())[0] for c in errors],
                         ['expression', 'expression', 'out_units'])

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
        self.calculator.add_data(self.expressions)
        result = self.calculator.convert()
        self.assertEqual(result.id, self.calculator.id)
        self.assertEqual(self.calculator.status, self.calculator.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.calculator.data))

    def test_computation_and_conversion(self):
        """
        Test computation
        """
        self.calculator.add_data(self.expression_to_unit)
        result = self.calculator.convert()
        self.assertEqual(result.id, self.calculator.id)
        self.assertEqual(self.calculator.status, self.calculator.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.calculator.data))
        self.assertEqual(result.detail[0].unit, 'pound')
        self.assertEqual(result.detail[1].unit, 'milligram')


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
        self.expression_to_unit = [
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
                ],
                'out_units': 'ton'
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
                ],
                'out_units': 'hundredweight'
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
        self.assertEqual(
            len(response.json().get('detail')),
            len(self.expressions))
        self.assertEqual(response.json().get('detail')[0]['magnitude'],
                         0.525)

    def test_convert_to_unit_request(self):
        """
        Test calculate API
        """
        client = APIClient()
        response = client.post(
            '/units/SI/formulas/calculate/',
            data={
                'data': self.expression_to_unit,
                'unit_system': 'SI',
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('detail')),
                         len(self.expression_to_unit))
        self.assertEqual(response.json().get('detail')[0]['unit'],
                         'ton')
        self.assertEqual(response.json().get('detail')[1]['unit'],
                         'hundredweight')

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
        self.assertEqual(response.json().get('status'),
                         ExpressionCalculator.INSERTING_STATUS)
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
        self.assertEqual(response.json().get('status'),
                         ExpressionCalculator.FINISHED)
        self.assertEqual(len(response.json().get('detail')),
                         2 * len(self.expressions))

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
        self.assertEqual(response.json().get('status'),
                         ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.get(f'/watch/{str(batch_id)}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'),
                         ExpressionCalculator.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
