"""
Permissions for Currency API
"""

from rest_framework import permissions


class CurrencyObjectPermission(permissions.BasePermission):
    """
    Permissions for Currency API
    """

    def has_object_permission(self, request, view, obj):
        """
        Read only permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
