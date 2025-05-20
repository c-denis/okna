from rest_framework import permissions
from django.contrib.auth.models import Group

class IsOperator(permissions.BasePermission):
    """
    Проверяет, что пользователь имеет роль Оператора.
    Операторы могут только создавать и просматривать свои заявки.
    """
    def has_permission(self, request, view):
        return request.user.role.name == 'operator' if hasattr(request.user, 'role') else False

class IsCoordinator(permissions.BasePermission):
    """
    Проверяет, что пользователь имеет роль Координатора.
    Координаторы могут назначать заявки и просматривать все данные кроме админских.
    """
    def has_permission(self, request, view):
        return request.user.role.name == 'coordinator' if hasattr(request.user, 'role') else False

class IsManager(permissions.BasePermission):
    """
    Проверяет, что пользователь имеет роль Менеджера (Мастера).
    Менеджеры могут обновлять статусы назначенных им заявок.
    """
    def has_permission(self, request, view):
        return request.user.role.name == 'manager' if hasattr(request.user, 'role') else False

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает полный доступ администраторам, остальным только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff
        )

class ActionBasedPermission(permissions.AllowAny):
    """
    Динамические разрешения в зависимости от действия.
    Используется в ViewSet для назначения разных permission_classes разным действиям.
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False