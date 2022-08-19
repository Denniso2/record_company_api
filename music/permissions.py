from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


# We need to run a celery or cron job daily to clear users when
# their subscription expires
class IsSubscribed(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Subscribed').exists() or request.user.is_staff
