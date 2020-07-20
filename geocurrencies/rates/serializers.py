from rest_framework import serializers
from .models import Rate


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = [
           'key',
           'currency',
           'base_currency',
           'start_date',
           'end_date',
           'value',
        ]