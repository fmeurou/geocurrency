from rest_framework import serializers


class UserSerializer(serializers.BaseSerializer):
    username = serializers.CharField()
    email = serializers.CharField()

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email
        }
