from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permitir el acceso unicamente a los usuarios con rol instructor
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.rol == 'Admin')