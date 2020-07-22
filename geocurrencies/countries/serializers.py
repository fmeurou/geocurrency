from rest_framework import serializers
from countryinfo import CountryInfo


class CountrySerializer(serializers.Serializer):
    """
    Serializer for Country
    """
    name = serializers.CharField(read_only=True)
    numeric = serializers.IntegerField(read_only=True)
    alpha_2 = serializers.CharField(read_only=True)
    alpha_3 = serializers.CharField(read_only=True)

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

    def get_region(self, obj) -> str:
        return CountryInfo(obj.alpha_2).region()

    def get_subregion(self, obj) -> str:
        return CountryInfo(obj.alpha_2).subregion()

    def get_tld(self, obj) -> str:
        return CountryInfo(obj.alpha_2).tld()

    def get_capital(self, obj) -> str:
        return CountryInfo(obj.alpha_2).capital()