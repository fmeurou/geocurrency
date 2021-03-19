"""
Core serializers
"""
from rest_framework import serializers


class UserSerializer(serializers.BaseSerializer):
    """
    Serialize Django Auth User
    """
    username = serializers.CharField()
    email = serializers.CharField()

    def to_representation(self, instance):
        """
        Representation of the user
        """
        return {
            'username': instance.username,
            'email': instance.email
        }
