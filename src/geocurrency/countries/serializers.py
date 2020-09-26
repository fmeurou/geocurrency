import pycountry
import gettext

from drf_yasg.utils import swagger_serializer_method
from pycountry import countries
from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.Serializer):
    """
    Serializer for Country
    """
    name = serializers.CharField(read_only=True)
    numeric = serializers.IntegerField(read_only=True)
    alpha_2 = serializers.CharField()
    alpha_3 = serializers.CharField(read_only=True)
    translated_name = serializers.SerializerMethodField()

    @staticmethod
    def validate_alpha2(alpha_2):
        if countries.get(alpha_2=alpha_2):
            return alpha_2
        else:
            raise serializers.ValidationError('Invalid country alpha_2')

    def create(self, validated_data):
        return Country(validated_data.get('alpha_2'))

    def update(self, instance, validated_data):
        country = Country(validated_data.get('alpha_2'))
        self.instance = country

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_translated_name(self, obj: Country) -> str:
        request = self.context.get('request', None)
        if request:
            try:
                language = request.GET.get('language', request.LANGUAGE_CODE)
                translation = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=[language])
                translation.install()
                return translation.gettext(obj.name)
            except FileNotFoundError:
                return obj.name
        else:
            return obj.name


class CountryDetailSerializer(serializers.Serializer):
    """
    Detailed Serializer for Country
    """
    name = serializers.CharField(read_only=True)
    numeric = serializers.IntegerField(read_only=True)
    alpha_2 = serializers.CharField(read_only=True)
    alpha_3 = serializers.CharField(read_only=True)
    region = serializers.SerializerMethodField()
    subregion = serializers.SerializerMethodField()
    tld = serializers.SerializerMethodField()
    capital = serializers.SerializerMethodField()
    unit_system = serializers.SerializerMethodField()
    translated_name = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_region(self, obj) -> str:
        return obj.region

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_subregion(self, obj) -> str:
        return obj.subregion

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_tld(self, obj) -> str:
        return obj.tld

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_capital(self, obj) -> str:
        return obj.capital

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_unit_system(self, obj) -> str:
        return obj.unit_system

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_translated_name(self, obj: Country) -> str:
        request = self.context.get('request', None)
        if request:
            try:
                language = request.GET.get('language', request.LANGUAGE_CODE)
                translation = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=[language])
                translation.install()
                return translation.gettext(obj.name)
            except FileNotFoundError:
                return obj.name
        else:
            return obj.name
