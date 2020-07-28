from datetime import date, datetime

from rest_framework import serializers

from .models import Amount


class AmountSerializer(serializers.Serializer):
    system = serializers.CharField()
    unit = serializers.CharField()
    value = serializers.FloatField()
    date_obj = serializers.DateField()

    @staticmethod
    def validate_system(system):
        from geocurrencies.units.models import UnitSystem
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


class UnitSystemListSerializer(serializers.Serializer):
    system_name = serializers.CharField()


class UnitSystemDetailSerializer(serializers.Serializer):
    system_name = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

    def get_dimensions(self, obj):
        return obj.dimensionalities


class UnitSerializer(serializers.Serializer):
    name = serializers.CharField()
    dimension = serializers.SerializerMethodField()

    def get_dimension(self, obj):
        return obj.readable_dimension
