from rest_framework import viewsets, permissions
from django.contrib.auth.models import Group
from ...models import User
from ..serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    Поддерживает все операции CRUD.
    Автоматически фильтрует queryset в зависимости от прав.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Фильтрация пользователей:
        - Обычные пользователи видят только себя
        - Координаторы видят операторов и менеджеров
        - Админы видят всех
        """
        user = self.request.user
        
        if user.is_superuser:
            return super().get_queryset()
        elif user.is_coordinator:
            return User.objects.filter(
                role__name__in=['operator', 'manager']
            )
        
        return User.objects.filter(id=user.id)
    
    def perform_create(self, serializer):
        """
        Автоматическая установка создателя пользователя.
        """
        serializer.save(created_by=self.request.user)