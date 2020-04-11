from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile
    """

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
        ]
