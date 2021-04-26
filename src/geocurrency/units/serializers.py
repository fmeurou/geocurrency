"""
Serializers for Units module
"""

import logging
from datetime import date, datetime

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from geocurrency.core.serializers import UserSerializer
from .models import Quantity, UnitConversionPayload, Dimension, \
    CustomUnit, Unit


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
        Validating unit requires knowledge of the system
        that might embark user information for
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
            raise serializers.ValidationError(
                'Invalid date format, use YYYY-MM-DD')
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
    dimensions = serializers.SerializerMethodField(
        label="Dimensions the unit belongs to")

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
    code = serializers.CharField(
        label="technical name of the unit (enclosed in brackets)")
    name = serializers.CharField(
        label="Human readable name of the unit")
    dimension = serializers.CharField(
        label="Mathematical expression of the dimension")
    base_unit = serializers.SerializerMethodField(
        label="Name of the base unit")

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
        instance.unit_system = validated_data.get(
            'system',
            instance.unit_system)
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
    data = QuantitySerializer(
        label="List of unit conversions",
        many=True,
        required=False)
    base_system = serializers.CharField(
        label="Unit system used for conversion",
        required=True)
    base_unit = serializers.CharField(
        label="Unit to express the result in",
        required=True)
    batch_id = serializers.CharField(
        label="User defined batch ID",
        required=False)
    key = serializers.CharField(
        label="User defined categorization key",
        required=False)
    eob = serializers.BooleanField(
        label="End of batch ? triggers the conversion",
        default=False)
    _errors = {}

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of a converson payload
        """
        super().is_valid(raise_exception=raise_exception)
        if not self.initial_data.get('data') and \
                (not self.initial_data.get('batch_id')
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
        self.base_system = validated_data.get(
            'base_system',
            instance.base_system)
        self.base_unit = validated_data.get('base_system', instance.base_unit)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance


class CustomUnitSerializer(serializers.ModelSerializer):
    """
    Serialize a custom unit
    """
    id = serializers.CharField(
        label="ID of the CustomUnit",
        read_only=True)
    user = UserSerializer(
        label="Owner of the unit",
        read_only=True)
    unit_system = serializers.CharField(
        label="Unit system of the unit",
        read_only=True)

    class Meta:
        """
        Meta
        """
        model = CustomUnit
        fields = [
            'id',
            'user',
            'key',
            'unit_system',
            'code',
            'name',
            'relation',
            'symbol',
            'alias']
