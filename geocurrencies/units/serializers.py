from rest_framework import serializers


class UnitSystemListSerializer(serializers.Serializer):
    name = serializers.CharField()


class UnitSystemDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

    def get_dimensions(self, obj):
        return obj.dimensionalities

class UnitSerializer(serializers.Serializer):
    name = serializers.CharField()
    dimension = serializers.SerializerMethodField()

    def get_dimension(self, obj):
        return obj.dimensionality_string