"""
List of serializers for Converters and Calculators
"""

from rest_framework import serializers

from .models import Batch, ConverterResultError, ConverterResultDetail, ConverterResult, \
    CalculationResult, CalculationResultError, CalculationResultDetail


class CalculationResultDetailSerializer(serializers.Serializer):
    """
    Serializer for the CalculationResultDetail class
    """
    expression = serializers.CharField()
    operands = serializers.JSONField()
    magnitude = serializers.FloatField()
    units = serializers.CharField()

    def create(self, validated_data):
        """
        Create a CalculationResultDetail object
        :param validated_data: cleaned data
        """
        return CalculationResultDetail(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultDetail object
        :param instance: CalculationResultDetail object
        :param validated_data: cleaned data
        """
        instance.expression = validated_data.get('expression', instance.expression)
        instance.operands = validated_data.get('operands', instance.variables)
        instance.date = validated_data.get('date', instance.date)
        return instance


class CalculationResultErrorSerializer(serializers.Serializer):
    """
    Serialiwer for the CalculationResultError class
    """
    expression = serializers.CharField()
    variables = serializers.JSONField()
    date = serializers.DateField()
    error = serializers.CharField()

    def create(self, validated_data):
        """
        Create a CalculationResultError object
        :param validated_data: cleaned data
        """
        return CalculationResultError(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultError object
        :param instance: CalculationResultError object
        :param validated_data: cleaned data
        """
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
        """
        Create a CalculationResult object
        :param validated_data: cleaned data
        """
        return CalculationResult(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResult object
        :param instance: CalculationResult object
        :param validated_data: cleaned data
        """
        instance.id = validated_data.get('id', instance.id)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class ConverterResultDetailSerializer(serializers.Serializer):
    """
    Serialize a ConverterResultDetail class
    """
    unit = serializers.CharField()
    original_value = serializers.FloatField()
    date = serializers.DateField()
    conversion_rate = serializers.FloatField()
    converted_value = serializers.FloatField()

    def create(self, validated_data):
        """
        Create a ConverterResultDetail object
        :param validated_data: cleaned data
        """
        return ConverterResultDetail(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a ConverterResultDetail object
        :param instance: ConverterResultDetail object
        :param validated_data: cleaned data
        """
        instance.unit = validated_data.get('unit', instance.unit)
        instance.original_value = validated_data.get('original_value', instance.original_value)
        instance.date = validated_data.get('date', instance.date)
        return instance


class ConverterResultErrorSerializer(serializers.Serializer):
    """
    Serializer for ConverterResultError
    """
    unit = serializers.CharField()
    original_value = serializers.FloatField()
    date = serializers.DateField()
    error = serializers.CharField()

    def create(self, validated_data):
        """
        Create a ConverterResultError object
        :param validated_data: cleaned data
        """
        return ConverterResultError(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a ConverterResultError object
        :param instance: ConverterResultError object
        :param validated_data: cleaned data
        """
        instance.unit = validated_data.get('unit', instance.unit)
        instance.original_value = validated_data.get('original_value', instance.original_value)
        instance.date = validated_data.get('date', instance.date)
        instance.error = validated_data.get('error', instance.error)
        return instance


class ConverterResultSerializer(serializers.Serializer):
    """
    Serializer for a ConverterResult
    """
    id = serializers.UUIDField()
    target = serializers.CharField()
    detail = ConverterResultDetailSerializer(many=True)
    sum = serializers.FloatField()
    status = serializers.CharField()
    errors = ConverterResultErrorSerializer(many=True)

    def create(self, validated_data):
        """
        Create a ConverterResult object
        :param validated_data: cleaned data
        """
        return ConverterResult(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a ConverterResult object
        :param instance: ConverterResult object
        :param validated_data: cleaned data
        """
        instance.id = validated_data.get('id', instance.id)
        instance.target = validated_data.get('target', instance.target)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.sum = validated_data.get('sum', instance.sum)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class BatchSerializer(serializers.Serializer):
    """
    Serializer for Batch
    """
    id = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        """
        Create a Batch object
        :param validated_data: cleaned data
        """
        return Batch(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a Batch
        :param instance: Batch object
        :param validated_data: cleaned data
        """
        instance.status = validated_data.get('status', instance.status)
        return instance
