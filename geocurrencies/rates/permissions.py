from rest_framework import permissions


class RateObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method.lower() in ['post', 'put', 'patch', 'delete'] and request.user == obj.user:
            return True
        return False
