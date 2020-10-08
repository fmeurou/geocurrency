import logging
from datetime import date, datetime

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Amount, UnitConversionPayload, Dimension


class UnitAmountSerializer(serializers.Serializer):
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
        return Amount(**validated_data)

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
    def get_units(self, obj):
        try:
            return obj.units
        except KeyError as e:
            logging.error(str(e))
            return None


class UnitSystemSerializer(serializers.Serializer):
    system_name = serializers.CharField()


class UnitConversionPayloadSerializer(serializers.Serializer):
    data = UnitAmountSerializer(many=True, required=False)
    base_system = serializers.CharField(required=True)
    base_unit = serializers.CharField(required=True)
    batch_id = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    eob = serializers.BooleanField(default=False)

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get('data') and (not self.initial_data.get('batch_id')
                                                  or (self.initial_data.get('batch_id')
                                                      and not self.initial_data.get('eob'))):
            raise serializers.ValidationError(
                'data has to be provided if batch_id is not provided or batch_id is provided and eob is False'
            )
        return super(UnitConversionPayloadSerializer, self).is_valid()

    @staticmethod
    def validate_base_system(value):
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    @staticmethod
    def validate_base_unit(value):
        from geocurrency.units.models import Unit
        if not Unit.is_valid(value):
            raise serializers.ValidationError('Invalid unit')
        return value

    def create(self, validated_data):
        return UnitConversionPayload(**validated_data)

    def update(self, instance, validated_data):
        self.data = validated_data.get('data', instance.data)
        self.base_system = validated_data.get('base_system', instance.base_system)
        self.base_unit = validated_data.get('base_system', instance.base_unit)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance
