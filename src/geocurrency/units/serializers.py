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
    system = serializers.CharField()
    unit = serializers.CharField()
    value = serializers.FloatField()
    date_obj = serializers.DateField()

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
    code = serializers.CharField()
    name = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

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
    code = serializers.CharField()
    name = serializers.CharField()
    dimension = serializers.CharField()
    base_unit = serializers.SerializerMethodField()

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
    units = UnitSerializer(many=True)

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
    data = QuantitySerializer(many=True, required=False)
    base_system = serializers.CharField(required=True)
    base_unit = serializers.CharField(required=True)
    batch_id = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    eob = serializers.BooleanField(default=False)

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
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    unit_system = serializers.CharField(read_only=True)

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
    name = serializers.CharField()
    value = serializers.CharField()
    unit = serializers.CharField()

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the operand
        """
        if not self.initial_data.get('name'):
            raise serializers.ValidationError("variable Name not set")
        if 'value' not in self.initial_data:
            raise serializers.ValidationError("variable Value not set")
        if 'unit' not in self.initial_data:
            raise serializers.ValidationError("variable Unit not set")
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

    def is_valid(self, unit_system: UnitSystem, raise_exception=False):
        """
        Check validity of expression with a specific UnitSystem
        :param unit_system: UnitSystem instance
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        for initial_exp in self.initial_data:
            ec = ExpressionSerializer(data=initial_exp)
            ec.is_valid(unit_system=unit_system)
            if ec.errors:
                self._errors.append(ec.errors)
        return not bool(self._errors)


class ExpressionSerializer(serializers.Serializer):
    """
    Serialize an expression
    """
    unit_system = None
    key = None
    expression = serializers.CharField(required=True)
    operands = OperandSerializer(many=True, required=True)

    class Meta:
        """
        Meta
        """
        list_serializer_class = ExpressionListSerializer

    def is_valid(self, unit_system: UnitSystem, raise_exception=False) -> bool:
        """
        Check if expression is valid
        :param unit_system: UnitSystem instance
        :param raise_exception: raise an exception instead of a list of errors
        """
        Q_ = unit_system.ureg.Quantity
        super().is_valid(raise_exception=raise_exception)
        try:
            operands = self.initial_data.get('operands')
            if not self.validate_operands(operands):
                self._errors['operands'] = "Invalid operands"
        except json.JSONDecodeError as e:
            self._errors['operands'] = f"Invalid operands json format: {e}"
        expression = self.initial_data.get('expression')
        if not expression:
            self._errors['expression'] = "Empty expression"
            return not bool(self._errors)
        # Validate syntax
        value_kwargs = {v['name']: v['value'] for v in operands}
        try:
            sympify(expression.format(**value_kwargs))
        except (SympifyError, KeyError) as e:
            self._errors['expression'] = f"Invalid operation"
        # Validate units
        units_kwargs = {v['name']: f"{v['value']} {v['unit']}" for v in operands}
        try:
            Q_(expression.format(**units_kwargs))
        except KeyError as e:
            self._errors['operands'] = "Missing operands"
        except pint.errors.DimensionalityError as e:
            self._errors['expression'] = "Incoherent dimension"
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    @staticmethod
    def validate_operands(value):
        """
        Validate Operand
        :param value: Obperand
        """
        for var in value:
            vs = OperandSerializer(data=var)
            vs.is_valid()
        return value

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
    unit_system = serializers.CharField(required=True)
    data = ExpressionSerializer(many=True, required=False)
    batch_id = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    eob = serializers.BooleanField(default=False)

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
