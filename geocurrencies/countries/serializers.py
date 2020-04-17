from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for Country
    """
    timezone = serializers.CharField()
    coordinates = serializers.CharField()
    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'alpha_2',
            'alpha_3',
            'formal_name',
            'capital',
            'continent',
            'dial',
            'region',
            'subregion',
            'dependency',
            'timezone',
            'coordinates'
        ]

        def get_timezone(self, obj):
            try:
                return getattr(obj, 'timezone', '')
            except AttributeError:
                return ''

        def get_coordinates(self, obj):
            try:
                return getattr(obj, 'coordinates', '')
            except AttributeError:
                return ''

