import json
import logging
from datetime import date, datetime

import pint
from drf_yasg.utils import swagger_serializer_method
from geocurrency.core.serializers import UserSerializer
from rest_framework import serializers
from sympy import sympify, SympifyError

from .models import Quantity, UnitConversionPayload, Dimension, \
    CustomUnit, Expression, CalculationPayload, UnitSystem, Operand


class QuantitySerializer(serializers.Serializer):
    system = serializers.CharField()
    unit = serializers.CharField()
    value = serializers.FloatField()
    date_obj = serializers.DateField()

    @staticmethod
    def validate_system(system):
        from .models import UnitSystem
        if not UnitSystem.is_valid(system):
            raise serializers.ValidationError('Invalid system')
        return system

    @staticmethod
    def validate_unit(unit):
        # Validating unit requires knowledge of the system
        # Let‘s say it is valid for now
        return unit

    @staticmethod
    def validate_date_obj(value):
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value

    def create(self, validated_data):
        return Quantity(**validated_data)

    def update(self, instance, validated_data):
        instance.system = validated_data.get('system', instance.system)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.value = validated_data.get('value', instance.value)
        instance.date_obj = validated_data.get('date_obj', instance.date_obj)
        return instance


class UnitSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_dimensions(self, obj):
        return str(obj.dimensions)


class DimensionSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    dimension = serializers.CharField()
    base_unit = serializers.SerializerMethodField()

    def create(self, validated_data):
        return Dimension(**validated_data)

    def update(self, instance, validated_data):
        instance.unit_system = validated_data.get('system', instance.unit_system)
        instance.code = validated_data.get('code', instance.code)
        instance.value = validated_data.get('name', instance.name)
        instance.dimension = validated_data.get('date_obj', instance.dimension)
        return instance

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_base_unit(self, obj):
        return obj.base_unit


class DimensionWithUnitsSerializer(DimensionSerializer):
    units = UnitSerializer(many=True)

    @swagger_serializer_method(serializer_or_field=UnitSerializer)
    def get_units(self, obj: Dimension):
        try:
            return obj.units()
        except KeyError as e:
            logging.error(str(e))
            return None


class UnitSystemSerializer(serializers.Serializer):
    system_name = serializers.CharField()


class UnitConversionPayloadSerializer(serializers.Serializer):
    data = QuantitySerializer(many=True, required=False)
    base_system = serializers.CharField(required=True)
    base_unit = serializers.CharField(required=True)
    batch_id = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    eob = serializers.BooleanField(default=False)

    def is_valid(self, raise_exception=False) -> bool:
        super().is_valid(raise_exception=raise_exception)
        if not self.initial_data.get('data') and (not self.initial_data.get('batch_id')
                                                  or (self.initial_data.get('batch_id')
                                                      and not self.initial_data.get('eob'))):
            self._errors = {
                'data': 'data has to be provided if batch_id is not provided'
                        'or batch_id is provided and eob is False'
            }

        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    @staticmethod
    def validate_base_system(value: str):
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    @staticmethod
    def validate_base_unit(value: str) -> str:
        from geocurrency.units.models import Unit
        if not Unit.is_valid(value):
            raise serializers.ValidationError('Invalid unit')
        return value

    def create(self, validated_data: {}):
        return UnitConversionPayload(**validated_data)

    def update(self, instance, validated_data: {}):
        self.data = validated_data.get('data', instance.data)
        self.base_system = validated_data.get('base_system', instance.base_system)
        self.base_unit = validated_data.get('base_system', instance.base_unit)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance


class CustomUnitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    unit_system = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUnit
        fields = ['user', 'key', 'unit_system', 'code', 'name', 'relation', 'symbol', 'alias']


class OperandSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
    unit = serializers.CharField()

    def is_valid(self, raise_exception=False) -> bool:
        if not self.initial_data.get('name'):
            raise serializers.ValidationError("variable Name not set")
        if 'value' not in self.initial_data:
            raise serializers.ValidationError("variable Value not set")
        if 'unit' not in self.initial_data:
            raise serializers.ValidationError("variable Unit not set")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return Operand(**validated_data)


class ExpressionListSerializer(serializers.ListSerializer):

    def is_valid(self, unit_system: UnitSystem, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        for initial_exp in self.initial_data:
            ec = ExpressionSerializer(data=initial_exp)
            ec.is_valid(unit_system=unit_system)
            if ec.errors:
                self._errors.append(ec.errors)
        return not bool(self._errors)


class ExpressionSerializer(serializers.Serializer):
    unit_system = None
    key = None
    expression = serializers.CharField(required=True)
    operands = OperandSerializer(many=True, required=True)

    class Meta:
        list_serializer_class = ExpressionListSerializer

    def is_valid(self, unit_system: UnitSystem, raise_exception=False) -> bool:
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
        for var in value:
            vs = OperandSerializer(data=var)
            vs.is_valid()
        return value

    def create(self, validated_data):
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
        instance.expression = validated_data.get('expression')
        instance.operands = validated_data.get('operands')
        return instance


class CalculationPayloadSerializer(serializers.Serializer):
    unit_system = serializers.CharField(required=True)
    data = ExpressionSerializer(many=True, required=False)
    batch_id = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    eob = serializers.BooleanField(default=False)

    def is_valid(self, raise_exception=False) -> bool:
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
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    def create(self, validated_data: {}):
        return CalculationPayload(**validated_data)

    def update(self, instance, validated_data: {}):
        self.data = validated_data.get('data', instance.data)
        self.unit_system = validated_data.get('unit_system', instance.unit_system)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance
