from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """A user is allowed to modify their own object e.g deposit..."""

    def has_object_permission(self, request, view, obj):
        if request.method and request.method not in permissions.SAFE_METHODS:
            return bool(obj.user == request.user)
        return super().has_object_permission(request, view, obj)
