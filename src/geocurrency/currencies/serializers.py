"""
Serializers for Currencies module
"""
from rest_framework import serializers

from .models import Currency


class CurrencySerializer(serializers.Serializer):
    """
    Serializer for Currency class
    """
    code = serializers.CharField(label="ISO-4217 code of the currency", read_only=True)
    name = serializers.CharField(label="Human readable name of the currency", read_only=True)
    currency_name = serializers.CharField(label="name of the currency", read_only=True)
    exponent = serializers.IntegerField(label="ISO-4217 exponent", read_only=True)
    number = serializers.IntegerField(label="ISO-4217 numeric identifier", read_only=True)
    value = serializers.CharField(read_only=True)
    symbol = serializers.SerializerMethodField(label="Symbol of the currency")

    @staticmethod
    def get_symbol(obj: Currency):
        """
        Get symbol from currency
        """
        return obj.symbol

    def create(self, validated_data: dict) -> Currency:
        """
        Returns a Currency object from cleaned data
        """
        return Currency(code=validated_data.get('code'))

    def update(self, instance: Currency, validated_data: dict) -> Currency:
        """
        No update
        """
        return instance
