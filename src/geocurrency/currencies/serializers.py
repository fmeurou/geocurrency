"""
Serializers for Currencies module
"""
from rest_framework import serializers

from .models import Currency


class CurrencySerializer(serializers.Serializer):
    """
    Serializer for Currency class
    """
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    currency_name = serializers.CharField(read_only=True)
    exponent = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField(read_only=True)
    value = serializers.CharField(read_only=True)
    symbol = serializers.SerializerMethodField()

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
