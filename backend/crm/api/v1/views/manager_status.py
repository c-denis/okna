from rest_framework import viewsets, permissions
from ...models import ManagerStatus
from ..serializers import ManagerStatusSerializer

class ManagerStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы со статусами менеджеров.
    Позволяет обновлять статусы в реальном времени.
    """
    queryset = ManagerStatus.objects.all()
    serializer_class = ManagerStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Фильтрация по текущему пользователю (для менеджеров)
        или все статусы (для координаторов и админов).
        """
        user = self.request.user
        
        if user.is_manager and hasattr(user, 'managerstatus'):
            return ManagerStatus.objects.filter(user=user)
        
        return super().get_queryset()
    
    def perform_update(self, serializer):
        """
        Автоматическая отправка уведомления при изменении статуса.
        """
        instance = serializer.save()
        
        if instance.status == 'free':
            NotificationService.send_status_notification(
                instance.user,
                "Вы свободны для принятия новых заявок"
            )