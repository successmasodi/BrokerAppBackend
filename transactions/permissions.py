from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
  message = " You're not a superuser"

  def has_permission(self, request, view):
    return request.user.is_superuser