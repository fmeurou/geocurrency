from rest_framework import serializers


class UnitSystemListSerializer(serializers.Serializer):
    system = serializers.CharField()


class UnitSystemDetailSerializer(serializers.Serializer):
    system = serializers.CharField()
    dimensions = serializers.SerializerMethodField()

    def get_dimensions(self, obj):
        return obj.dimensionalities


class UnitSerializer(serializers.Serializer):
    name = serializers.CharField()
    dimension = serializers.SerializerMethodField()

    def get_dimension(self, obj):
        return obj.readable_dimension
