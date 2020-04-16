from rest_framework import serializers
from .models import CurrencyModel
from geocurrencies.countries.serializers import CountrySerializer


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyModel
        fields = ['name', 'code', 'exponent']

