"""
Permissions for CustomUnit APIs
"""

from rest_framework import permissions


class CustomUnitObjectPermission(permissions.BasePermission):
    """
    Permissions for CustomUnit API
    """

    def has_object_permission(self, request, view, obj):
        """
        Limit creation and modification tu logged in users
        """
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        elif request.method.lower() in ['put', 'patch', 'delete'] and request.user == obj.user:
            return True
        return False
