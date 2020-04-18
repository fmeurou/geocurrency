from datetime import datetime
from pytz import timezone
from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for Country
    """
    current_time = serializers.SerializerMethodField()
    timezone = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()

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

    def get_current_time(self, obj):
        try:
            base_time = datetime.utcnow()
            tz_info = getattr(obj, 'timezone', '')
            if not tz_info:
                return ''
            tz = timezone(tz_info)
            return base_time.astimezone(tz).strftime('%Y-%m-%d %H:%M')
        except AttributeError:
            return ''

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
            'current_time',
            'coordinates'
        ]


