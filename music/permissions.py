from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsSubscribed(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Subscribed').exists() or request.user.is_staff
