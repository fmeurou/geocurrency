from rest_framework import serializers

from .models import Currency, CurrencyNotFoundError


class CurrencySerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    currency_name = serializers.CharField(read_only=True)
    exponent = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField(read_only=True)
    value = serializers.CharField(read_only=True)
    symbol = serializers.SerializerMethodField()

    def get_symbol(self, obj):
        return obj.symbol

    def create(self, validated_data):
        return Currency(code=validated_data.get('code'))

