from datetime import datetime, date

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rate, Amount, BulkRate, RateConversionPayload


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


class RateAmountSerializer(serializers.Serializer):
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


class RateConversionPayloadSerializer(serializers.Serializer):
    data = RateAmountSerializer(many=True, required=False)
    target = serializers.CharField(required=True)
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
        return super(RateConversionPayloadSerializer, self).is_valid()

    @staticmethod
    def validate_target(value):
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    def create(self, validated_data):
        return RateConversionPayload(**validated_data)

    def update(self, instance, validated_data):
        self.data = validated_data.get('data', instance.data)
        self.target = validated_data.get('target', instance.target)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance



