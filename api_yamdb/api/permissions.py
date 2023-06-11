from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    allowed = ("admin",)

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role in self.allowed
        ) or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == "admin"
        ) or request.method in permissions.SAFE_METHODS


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role != "user"
            or (request.user.role == "user" and obj.author == request.user)
        )
