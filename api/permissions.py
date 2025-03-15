from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsOwner(permissions.IsAuthenticated):
    """A user is allowed to modify their own object e.g deposit..."""

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)
