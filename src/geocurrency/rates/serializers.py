from datetime import datetime, date

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rate, Amount, BulkRate


class UserSerializer(serializers.BaseSerializer):
    username = serializers.CharField()
    email = serializers.CharField()

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email
        }


class BulkSerializer(serializers.Serializer):
    base_currency = serializers.CharField(max_length=3, required=True)
    currency = serializers.CharField(max_length=3, required=True)
    value = serializers.FloatField(required=True)
    key = serializers.CharField(required=True)
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=False)

    def create(self, validated_data):
        return BulkRate(**validated_data)

    def update(self, instance, validated_data):
        instance.base_currency = validated_data.get('base_currency', instance.base_currency)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.value = validated_data.get('value', instance.value)
        instance.key = validated_data.get('key', instance.key)
        instance.from_date = validated_data.get('key', instance.from_date)
        instance.to_date = validated_data.get('key', instance.to_date)
        return instance

    @staticmethod
    def validate_currency(value):
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_base_currency(value):
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_from_date(value):
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value

    @staticmethod
    def validate_to_date(value):
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value


class RateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer(read_only=True)

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
        from geocurrency.currencies.models import Currency
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
        instance.currency = validated_data.get('currency', instance.email)
        instance.amount = validated_data.get('amount', instance.content)
        instance.date_obj = validated_data.get('date_obj', instance.created)
        return instance
