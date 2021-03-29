"""
Serializers for Units module
"""

import json
import logging
from datetime import date, datetime

import pint
from drf_yasg.utils import swagger_serializer_method
from geocurrency.core.serializers import UserSerializer
from rest_framework import serializers
from sympy import sympify, SympifyError

from .models import Quantity, UnitConversionPayload, Dimension, \
    CustomUnit, Expression, CalculationPayload, UnitSystem, Operand, Unit


class QuantitySerializer(serializers.Serializer):
    """
    Serialize a Quantity
    """
    system = serializers.CharField(label="Unit system of the Quantity")
    unit = serializers.CharField(label="Units of the quantity")
    value = serializers.FloatField(label="Magnitude of the quantity")
    date_obj = serializers.DateField(label="date of conversion")

    @staticmethod
    def validate_system(system):
        """
        Validate unit system by name
        :param system: system name
        """
        from .models import UnitSystem
        if not UnitSystem.is_valid(system):
            raise serializers.ValidationError('Invalid system')
        return system

    @staticmethod
    def validate_unit(unit):
        """
        Validating unit requires knowledge of the system that might embark user information for
        custom units
        Let‘s say it is valid for now
        """
        return unit

    @staticmethod
    def validate_date_obj(value):
        """
        Validate date
        :param value:
        """
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value

    def create(self, validated_data):
        """
        Create a Quantity object
        :param validated_data: cleaned data
        """
        return Quantity(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a Quantity object
        :param instance: Quantity object
        :param validated_data: cleaned data
        """
        instance.system = validated_data.get('system', instance.system)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.value = validated_data.get('value', instance.value)
        instance.date_obj = validated_data.get('date_obj', instance.date_obj)
        return instance


class UnitSerializer(serializers.Serializer):
    """
    Unit class serializer
    """
    code = serializers.CharField(label="Technical name of the unit")
    name = serializers.CharField(label="Human readable name of the unit")
    dimensions = serializers.SerializerMethodField(label="Dimensions the unit belongs to")

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_dimensions(self, obj):
        """
        Get dimension of unit
        :param obj: Unit instance
        """
        return str(obj.dimensions)


class DimensionSerializer(serializers.Serializer):
    """
    Dimension class serializer
    """
    code = serializers.CharField(label="technical name of the unit (enclosed in brackets)")
    name = serializers.CharField(label="Human readable name of the unit")
    dimension = serializers.CharField(label="Mathematical expression of the dimension")
    base_unit = serializers.SerializerMethodField(label="Name of the base unit")

    def create(self, validated_data):
        """
        Create a Dimension object from cleaned data
        :param validated_data: cleaned data
        """
        return Dimension(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a Dimension object
        :param instance: Dimension object
        :param validated_data: cleaned data
        """
        instance.unit_system = validated_data.get('system', instance.unit_system)
        instance.code = validated_data.get('code', instance.code)
        instance.value = validated_data.get('name', instance.name)
        instance.dimension = validated_data.get('date_obj', instance.dimension)
        return instance

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_base_unit(self, obj: Dimension) -> Unit:
        """
        Get base unit for dimension object
        :param obj: Dimension object
        """
        return obj.base_unit


class DimensionWithUnitsSerializer(DimensionSerializer):
    """
    Serialize a Dimension including associated units
    """
    units = UnitSerializer(label="Units of this dimension", many=True)

    @swagger_serializer_method(serializer_or_field=UnitSerializer)
    def get_units(self, obj: Dimension) -> [Unit]:
        """
        Get units for this dimension
        """
        try:
            return obj.units()
        except KeyError as e:
            logging.error(str(e))
            return []


class UnitSystemSerializer(serializers.Serializer):
    """
    Serialize a UnitSystem
    """
    system_name = serializers.CharField()


class UnitConversionPayloadSerializer(serializers.Serializer):
    """
    Serialize a UnitConversionPayload
    """
    data = QuantitySerializer(label="List of unit conversions", many=True, required=False)
    base_system = serializers.CharField(label="Unit system used for conversion", required=True)
    base_unit = serializers.CharField(label="Unit to express the result in", required=True)
    batch_id = serializers.CharField(label="User defined batch ID", required=False)
    key = serializers.CharField(label="User defined categorization key", required=False)
    eob = serializers.BooleanField(label="End of batch ? triggers the conversion", default=False)
    _errors = {}

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of a converson payload
        """
        super().is_valid(raise_exception=raise_exception)
        if not self.initial_data.get('data') and (not self.initial_data.get('batch_id')
                                                  or (self.initial_data.get('batch_id')
                                                      and not self.initial_data.get('eob'))):
            self._errors = {
                'data': 'data has to be provided if batch_id is not provided'
                        'or batch_id is provided and eob is False'
            }

        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        return not bool(self._errors)

    @staticmethod
    def validate_base_system(value: str):
        """
        Validate unit system
        :param value: unit system name
        """
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    @staticmethod
    def validate_base_unit(value: str) -> str:
        """
        Validate base unit
        :param value: name of unit
        """
        from geocurrency.units.models import Unit
        if not Unit.is_valid(value):
            raise serializers.ValidationError('Invalid unit')
        return value

    def create(self, validated_data: {}) -> UnitConversionPayload:
        """
        Create a UnitConversionPayload
        :param validated_data: cleaned data
        """
        return UnitConversionPayload(**validated_data)

    def update(self, instance, validated_data: {}) -> UnitConversionPayload:
        """
        Update a UnitConversionPayload
        :param instance: UnitConversionPayload
        :param validated_data: cleaned data
        """
        self.data = validated_data.get('data', instance.data)
        self.base_system = validated_data.get('base_system', instance.base_system)
        self.base_unit = validated_data.get('base_system', instance.base_unit)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance


class CustomUnitSerializer(serializers.ModelSerializer):
    """
    Serialize a custom unit
    """
    id = serializers.CharField(label="ID of the CustomUnit", read_only=True)
    user = UserSerializer(label="Owner of the unit", read_only=True)
    unit_system = serializers.CharField(label="Unit system of the unit", read_only=True)

    class Meta:
        """
        Meta
        """
        model = CustomUnit
        fields = ['id', 'user', 'key', 'unit_system', 'code', 'name', 'relation', 'symbol', 'alias']


class OperandSerializer(serializers.Serializer):
    """
    Serialize an Operand
    """
    name = serializers.CharField(label="Name of the operand in the expression",
                                 help_text="{a} in an expression should have an operand named 'a'")
    value = serializers.FloatField(label="Value of the operand as a float")
    unit = serializers.CharField(label="Units of the operand as a string")

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the operand
        """
        if not self.initial_data.get('name'):
            raise serializers.ValidationError("operand Name not set")
        if 'value' not in self.initial_data:
            raise serializers.ValidationError("operand Value not set")
        try:
            float(self.initial_data['value'])
        except ValueError as e:
            raise serializers.ValidationError("invalid operand value") from e
        if 'unit' not in self.initial_data:
            raise serializers.ValidationError("operand Unit not set")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        """
        Create an Operand object
        :param validated_data: cleaned date
        """
        return Operand(**validated_data)


class ExpressionListSerializer(serializers.ListSerializer):
    """
    Serialize a list of Expressions
    """

    def is_valid(self, unit_system: UnitSystem, dimensions_only=False, raise_exception=False):
        """
        Check validity of expression with a specific UnitSystem
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only check dimensionality, not actual units
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        for initial_exp in self.initial_data:
            ec = ExpressionSerializer(data=initial_exp)
            ec.is_valid(unit_system=unit_system, dimensions_only=dimensions_only)
            if ec.errors:
                self._errors.append(ec.errors)
        return not bool(self._errors)


class ExpressionSerializer(serializers.Serializer):
    """
    Serialize an expression
    """
    unit_system = None
    key = None
    expression = serializers.CharField(label="Mathematical expression to evaluate", required=True,
                                       help_text="Operands must be placed between curly braces."
                                                 "A recommended expression format "
                                                 "would be '{a}+{b}*{c}'")
    operands = OperandSerializer(label="List of operands", many=True, required=True)

    class Meta:
        """
        Meta
        """
        list_serializer_class = ExpressionListSerializer

    def is_valid(self, unit_system: UnitSystem,
                 raise_exception=False,
                 dimensions_only=False) -> bool:
        """
        Check if expression is valid
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only test dimensions
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        operands = self.operands_validation(
            operands=self.initial_data.get('operands')
        )
        expression = self.expression_validation(
            expression=self.initial_data.get('expression'),
            operands=operands
        )
        if expression:
            if dimensions_only:
                self.dimensions_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands
                )
            else:
                self.units_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands
                )
        if self._errors and raise_exception:
            raise serializers.ValidationError(self._errors)
        return not bool(self._errors)

    def units_validation(self, unit_system: UnitSystem, expression: str, operands: [Operand]):
        """
        Validate units based on the units of the operands
        """
        # Validate units
        q_ = unit_system.ureg.Quantity
        units_kwargs = {v['name']: f"{v['value']} {v['unit']}" for v in operands}
        try:
            return q_(expression.format(**units_kwargs))
        except KeyError as e:
            self._errors['operands'] = "Missing operands"
        except pint.errors.DimensionalityError as e:
            self._errors['expression'] = "Incoherent dimension"
        return None

    def dimensions_validation(self, unit_system: UnitSystem, expression: str, operands: [Operand]):
        """
        Validate units dimensions based on get_unit of the operands
        """
        Q_ = unit_system.ureg.Quantity
        operand_objs = [Operand(name=v['name'], value=v['value'], unit=v['unit']) for v in operands]
        units_kwargs = {v.name: f"{v.value} {v.get_unit(unit_system)}" for v in operand_objs}
        try:
            return Q_(expression.format(**units_kwargs))
        except KeyError as e:
            self._errors['operands'] = "Missing operands"
        except pint.errors.DimensionalityError as e:
            self._errors['expression'] = "Incoherent dimension"
        return None

    def expression_validation(self, expression: str, operands: [Operand]):
        """
        Check validity of expression
        """
        if not expression:
            self._errors['expression'] = "Empty expression"
        # Validate syntax
        value_kwargs = {v['name']: v['value'] for v in operands}
        try:
            sympify(expression.format(**value_kwargs))
        except (SympifyError, KeyError) as e:
            self._errors['expression'] = f"Invalid operation"
        return expression

    def operands_validation(self, operands):
        """
        Validate Operand
        :param operands: Operand
        """
        errors = []
        try:
            for var in operands:
                vs = OperandSerializer(data=var)
                vs.is_valid()
                if vs.errors:
                    errors.append(vs.errors)
            if errors:
                self._errors['operands'] = errors
        except json.JSONDecodeError as e:
            self._errors['operands'] = f"Invalid operands json format: {e}"
        return operands

    def create(self, validated_data):
        """
        Create an Expression
        :param validated_data: cleaned data
        """
        operands = []
        for var in validated_data.get('operands'):
            vs = OperandSerializer(data=var)
            if vs.is_valid():
                operands.append(vs.create(vs.validated_data))
        return Expression(
            expression=validated_data.get('expression'),
            operands=operands
        )

    def update(self, instance, validated_data):
        """
        Update Expression
        :param instance: Expression object
        :param validated_data: cleaned data
        """
        instance.expression = validated_data.get('expression')
        instance.operands = validated_data.get('operands')
        return instance


class CalculationPayloadSerializer(serializers.Serializer):
    """
    Serializer for CalculationPayload
    """
    unit_system = serializers.CharField(label="Unit system to evaluate in", required=True)
    data = ExpressionSerializer(label="Payload of expressions", many=True, required=False)
    batch_id = serializers.CharField(label="User defined ID of the batch of evaluations",
                                     required=False)
    key = serializers.CharField(label="User defined categorization key", required=False)
    eob = serializers.BooleanField(label="End of batch ? triggers the evaluation", default=False)

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the payload
        """
        if not self.initial_data.get('data') and (not self.initial_data.get('batch_id')
                                                  or (self.initial_data.get('batch_id')
                                                      and not self.initial_data.get('eob'))):
            raise serializers.ValidationError(
                'data has to be provided if batch_id is not provided '
                'or batch_id is provided and eob is False'
            )
        return super().is_valid(raise_exception=raise_exception)

    @staticmethod
    def validate_unit_system(value: str):
        """
        Validate unit system
        :param value: unit system name
        """
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    def create(self, validated_data: {}):
        """
        Create CalculationPayload from cleaned data
        :param validated_data: cleaned data
        """
        return CalculationPayload(**validated_data)

    def update(self, instance, validated_data: {}):
        """
        Update a CalculationPayload from cleaned data
        :param instance: CalculationPayload object
        :param validated_data: cleaned data
        """
        self.data = validated_data.get('data', instance.data)
        self.unit_system = validated_data.get('unit_system', instance.unit_system)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance
