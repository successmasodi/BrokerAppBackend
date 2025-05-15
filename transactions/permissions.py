from rest_framework import permissions


class IsStaffOnly(permissions.BasePermission):
    message = "You're not a superuser"

    def has_permission(self, request, view):
        return request.user.is_staff
