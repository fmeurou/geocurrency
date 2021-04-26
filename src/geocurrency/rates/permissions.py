"""
Permissions for Rate APIs
"""
from rest_framework import permissions


class RateObjectPermission(permissions.BasePermission):
    """
    Permissions for /rates APIs
    """

    def has_object_permission(self, request, view, obj):
        """
        Limit modifications to authenticated users
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            if request.method == 'POST':
                return True
            elif request.method.lower() in ['put', 'patch', 'delete'] and \
                    request.user == obj.user:
                return True
        return False
