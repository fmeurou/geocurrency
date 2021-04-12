"""
List of serializers for Converters and Calculators
"""

from rest_framework import serializers

from .models import Batch, ConverterResultError, ConverterResultDetail, ConverterResult







class ConverterResultDetailSerializer(serializers.Serializer):
    """
    Serialize a ConverterResultDetail class
    """
    unit = serializers.CharField(label="Unit of conversion")
    original_value = serializers.FloatField(label="Original value to convert")
    date = serializers.DateField(label="Date of conversion")
    conversion_rate = serializers.FloatField(label="Conversion rate")
    converted_value = serializers.FloatField(label="Resulting value")

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
    unit = serializers.CharField(label="Unit of conversion")
    original_value = serializers.FloatField(label="Original value")
    date = serializers.DateField(label="Date of conversion")
    error = serializers.CharField(label="Error during conversion")

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
    id = serializers.UUIDField(label="ID of the batch")
    target = serializers.CharField(label="Target conversion")
    detail = ConverterResultDetailSerializer(label="Details of conversion", many=True)
    sum = serializers.FloatField(label="Sum of conversions")
    status = serializers.CharField(label="Status of the conversion")
    errors = ConverterResultErrorSerializer(label="Errors during conversions", many=True)

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
    id = serializers.CharField(label="Batch unique identifier")
    status = serializers.CharField(label="Status of the batch")

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
