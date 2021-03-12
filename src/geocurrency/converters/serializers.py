from rest_framework import serializers

from .models import Batch, ConverterResultError, ConverterResultDetail, ConverterResult, \
    CalculationResult, CalculationResultError, CalculationResultDetail


class CalculationResultDetailSerializer(serializers.Serializer):
    expression = serializers.CharField()
    operands = serializers.JSONField()
    magnitude = serializers.FloatField()
    units = serializers.CharField()

    def create(self, validated_data):
        return CalculationResultDetail(**validated_data)

    def update(self, instance, validated_data):
        instance.expression = validated_data.get('expression', instance.expression)
        instance.operands = validated_data.get('operands', instance.variables)
        instance.date = validated_data.get('date', instance.date)
        return instance


class CalculationResultErrorSerializer(serializers.Serializer):
    expression = serializers.CharField()
    variables = serializers.JSONField()
    date = serializers.DateField()
    error = serializers.CharField()

    def create(self, validated_data):
        return CalculationResultError(**validated_data)

    def update(self, instance, validated_data):
        instance.expression = validated_data.get('expression', instance.expression)
        instance.operands = validated_data.get('operands', instance.variables)
        instance.date = validated_data.get('date', instance.date)
        instance.error = validated_data.get('error', instance.error)
        return instance


class CalculationResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    detail = CalculationResultDetailSerializer(many=True)
    status = serializers.CharField()
    errors = CalculationResultErrorSerializer(many=True)

    def create(self, validated_data):
        return CalculationResult(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class ConverterResultDetailSerializer(serializers.Serializer):
    unit = serializers.CharField()
    original_value = serializers.FloatField()
    date = serializers.DateField()
    conversion_rate = serializers.FloatField()
    converted_value = serializers.FloatField()

    def create(self, validated_data):
        return ConverterResultDetail(**validated_data)

    def update(self, instance, validated_data):
        instance.unit = validated_data.get('unit', instance.unit)
        instance.original_value = validated_data.get('original_value', instance.original_value)
        instance.date = validated_data.get('date', instance.date)
        return instance


class ConverterResultErrorSerializer(serializers.Serializer):
    unit = serializers.CharField()
    original_value = serializers.FloatField()
    date = serializers.DateField()
    error = serializers.CharField()

    def create(self, validated_data):
        return ConverterResultError(**validated_data)

    def update(self, instance, validated_data):
        instance.unit = validated_data.get('unit', instance.unit)
        instance.original_value = validated_data.get('original_value', instance.original_value)
        instance.date = validated_data.get('date', instance.date)
        instance.error = validated_data.get('error', instance.error)
        return instance


class ConverterResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    target = serializers.CharField()
    detail = ConverterResultDetailSerializer(many=True)
    sum = serializers.FloatField()
    status = serializers.CharField()
    errors = ConverterResultErrorSerializer(many=True)

    def create(self, validated_data):
        return ConverterResult(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.target = validated_data.get('target', instance.target)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.sum = validated_data.get('sum', instance.sum)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class BatchSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        return Batch(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        return instance
