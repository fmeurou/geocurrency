from rest_framework import serializers

from .models import Batch, ConverterResultError, ConverterResultDetail, ConverterResult


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
        instance.error = validated_data.get('error', instance.error)
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
