from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsOwner(permissions.IsAuthenticated):
    """A user is allowed to modify their own object e.g deposit..."""

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method  and request.method not in permissions.SAFE_METHODS:
            return bool(request.user.is_staff)
        return super().has_permission(request, view)