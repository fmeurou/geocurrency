"""
REST permissions
"""

from rest_framework import permissions


class CountryObjectPermission(permissions.BasePermission):
    """
    RO Permissions for Country objects
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """
        check permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
