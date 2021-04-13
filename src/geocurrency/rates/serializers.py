"""
Serializers for Rats module
"""
from datetime import datetime, date

from geocurrency.core.serializers import UserSerializer
from rest_framework import serializers

from .models import Rate, Amount, BulkRate, RateConversionPayload


class BulkSerializer(serializers.Serializer):
    """
    Serializer for Bulk serializer
    """
    base_currency = serializers.CharField(label="Currency to convert to", max_length=3,
                                          required=True)
    currency = serializers.CharField(label="Currency to convert from", max_length=3, required=True)
    value = serializers.FloatField(label="rate value", required=True)
    key = serializers.CharField(label="User defined categorization ID", required=True)
    from_date = serializers.DateField(label="Date to create the rate from", required=True)
    to_date = serializers.DateField(label="Date to create the rate to", required=False)

    def create(self, validated_data):
        """
        Create a BulkRate object
        """
        return BulkRate(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a BulkRate object
        """
        instance.base_currency = validated_data.get('base_currency', instance.base_currency)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.value = validated_data.get('value', instance.value)
        instance.key = validated_data.get('key', instance.key)
        instance.from_date = validated_data.get('key', instance.from_date)
        instance.to_date = validated_data.get('key', instance.to_date)
        return instance

    @staticmethod
    def validate_currency(value):
        """
        validate currency
        :param value: Currency
        """
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_base_currency(value):
        """
        Validate base currency
        :param value: Currency
        """
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_from_date(value):
        """
        Validate from_date
        :param value: date
        """
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value

    @staticmethod
    def validate_to_date(value):
        """
        Validate to_date
        :param value: date
        """
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value


class RateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(label="ID of the rate")
    user = UserSerializer(label="Owner of the rate", read_only=True)

    class Meta:
        model = Rate
        fields = [
            'id',
            'user',
            'key',
            'currency',
            'base_currency',
            'value_date',
            'value',
        ]


class RateStatItemSerializer(serializers.Serializer):
    """
    Rate statistics item for conversion
    """
    currency = serializers.CharField(label="Currency to convert from", read_only=True)
    base_currency = serializers.CharField(label="Currency to convert to", read_only=True)
    period = serializers.CharField(label="Period over which to aggregate", read_only=True)
    avg = serializers.FloatField(label="Average value", read_only=True)
    max = serializers.FloatField(label="Max value", read_only=True)
    min = serializers.FloatField(label="Min value", read_only=True)
    std_dev = serializers.FloatField(label="Standard deviation", read_only=True)


class RateStatSerializer(serializers.Serializer):
    """
    Rate statistics used in conversion
    """
    key = serializers.CharField(label="User defined categorization key", read_only=True)
    period = serializers.CharField(label="Period over which to aggregate", read_only=True)
    from_date = serializers.DateField(label="start aggregation date", read_only=True)
    to_date = serializers.DateField(label="end aggregation date", read_only=True)
    results = RateStatItemSerializer(label="List of results", many=True, read_only=True)


class RateAmountSerializer(serializers.Serializer):
    """
    Rate amount used in conversion
    """
    currency = serializers.CharField(label="Currency of the amount")
    amount = serializers.FloatField(label="Value to convert")
    date_obj = serializers.DateField(label="Date of conversion")

    @staticmethod
    def validate_currency(value):
        """
        validate currency
        :param value: Currency
        """
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    @staticmethod
    def validate_amount(value):
        """
        validate amount
        :param value: Amount
        """
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError('Invalid number')
        return value

    @staticmethod
    def validate_date_obj(value):
        """
        Validate date
        :param value: date
        """
        if isinstance(value, date):
            return value
        try:
            datetime.strptime(value, 'YYYY-MM-DD')
        except ValueError:
            raise serializers.ValidationError('Invalid date format, use YYYY-MM-DD')
        return value

    def create(self, validated_data: dict) -> Amount:
        """
        Create Amount object
        :param validated_data: cleaned data
        """
        return Amount(**validated_data)

    def update(self, instance: Amount, validated_data: dict):
        """
        Update Amount object
        :param instance: Amount
        :param validated_data: cleaned date
        """
        instance.currency = validated_data.get('currency', instance.email)
        instance.amount = validated_data.get('amount', instance.content)
        instance.date_obj = validated_data.get('date_obj', instance.created)
        return instance


class RateConversionPayloadSerializer(serializers.Serializer):
    """
    Serialize a conversion payload
    """
    data = RateAmountSerializer(label="Amounts to convert", many=True, required=False)
    target = serializers.CharField(label="Target currency", required=True)
    batch_id = serializers.CharField(label="User defined batch ID", required=False)
    key = serializers.CharField(label="User defined categorization key", required=False)
    eob = serializers.BooleanField(label="End of batch? Triggers the conversion", default=False)

    def is_valid(self, raise_exception=False):
        """
        Check validity of the payload
        """
        if not self.initial_data.get('data') and (not self.initial_data.get('batch_id')
                                                  or (self.initial_data.get('batch_id')
                                                      and not self.initial_data.get('eob'))):
            raise serializers.ValidationError(
                'data has to be provided if batch_id '
                'is not provided or batch_id is provided and eob is False'
            )
        return super(RateConversionPayloadSerializer, self).is_valid()

    @staticmethod
    def validate_target(value: str):
        """
        Validate target currency
        :param value: string
        """
        from geocurrency.currencies.models import Currency
        if not Currency.is_valid(value):
            raise serializers.ValidationError('Invalid currency')
        return value

    def create(self, validated_data: dict) -> RateConversionPayload:
        """
        Create a RateConversionPayload from serialized data
        :param validated_data: cleaned data
        """
        return RateConversionPayload(**validated_data)

    def update(self, instance, validated_data):
        """
        Update RateConversionPayload from serialized data
        :param instance: RateConversionPayload object
        :param validated_data: cleaned data
        """
        self.data = validated_data.get('data', instance.data)
        self.target = validated_data.get('target', instance.target)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance
