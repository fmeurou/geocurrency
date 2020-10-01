from datetime import date, datetime

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Amount, UnitConversionPayload


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
    family = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_dimensions(self, obj):
        return str(obj.dimension)


class UnitFamilySerializer(serializers.Serializer):
    family = serializers.CharField()
    units = UnitSerializer(many=True)


class UnitSystemListSerializer(serializers.Serializer):
    system_name = serializers.CharField()


class UnitSystemDetailSerializer(serializers.Serializer):
    system_name = serializers.CharField()
    dimensions = serializers.SerializerMethodField()
    units = UnitFamilySerializer(many=True)

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_dimensions(self, obj):
        return obj.dimensionalities

    @swagger_serializer_method(serializer_or_field=UnitSerializer)
    def get_units(self, obj):
        return obj.units_per_family()


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
