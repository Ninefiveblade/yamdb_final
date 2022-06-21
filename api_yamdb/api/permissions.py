"""Пермишены приложения API."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Пермишен доступа только администратору."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin) or (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """Пермишен доступа администратора
    или доступно только для чтения.
    has_permission - переопределение
    метода BasePermission, для
    настроек с кастомными юзерами.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin) or (
            request.user.is_authenticated
            and request.user.is_superuser
        ) or request.method in SAFE_METHODS


class IsStaffOrOwner(BasePermission):
    """Пермишен доступа персонала и пользователя.
    Переопределенные методы:
    Общий -has_permission
    Объектный - has_object_permission.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin
                    or request.user.is_moderator
                )
            )
            or request.user.is_superuser
        )
