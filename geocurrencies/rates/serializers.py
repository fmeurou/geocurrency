from datetime import datetime, date
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rate, Amount, Batch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class RateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer()

    class Meta:
        model = Rate
        fields = [
            'id',
            'user',
            'key',
            'currency',
            'base_currency',
            'value_date',
            'value',
        ]


class AmountSerializer(serializers.Serializer):
    currency = serializers.CharField()
    amount = serializers.FloatField()
    date_obj = serializers.DateField()

    @staticmethod
    def validate_currency(value):
        from geocurrencies.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_amount(value):
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError('Invalid number')
        return value

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
        instance.email = validated_data.get('currency', instance.email)
        instance.content = validated_data.get('amount', instance.content)
        instance.created = validated_data.get('date_obj', instance.created)
        return instance


class BatchSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        return Batch(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        return instance


class ErrorSerializer(serializers.Serializer):
    currency = serializers.CharField()
    original_amount = serializers.FloatField()
    date = serializers.DateField()


class DetailSerializer(serializers.Serializer):
    currency = serializers.CharField()
    original_amount = serializers.FloatField()
    date = serializers.DateField()
    rate = serializers.FloatField()
    converted_amount = serializers.FloatField()


class ResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    target = serializers.CharField()
    detail = DetailSerializer(many=True)
    sum = serializers.FloatField()
    status = serializers.CharField()
    errors = ErrorSerializer(many=True)
