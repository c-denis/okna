from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from crm.models import Order
from ..serializers import OrderSerializer
from crm.services.order_service import OrderService
from crm.services.notification_service import NotificationService

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заявками.
    Поддерживает все операции CRUD и специальные действия:
    - Назначение менеджера
    - Изменение статусов
    - Добавление в черный список
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Фильтрация заявок в зависимости от роли пользователя:
        - Операторы видят только свои заявки
        - Менеджеры видят назначенные им заявки
        - Координаторы и админы видят все
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.is_operator:
            return queryset.filter(created_by=user)
        elif user.is_manager:
            return queryset.filter(assigned_to=user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Назначение заявки менеджеру.
        Требует координаторских прав.
        """
        order = self.get_object()
        manager_id = request.data.get('manager_id')
        
        if not manager_id:
            return Response(
                {'error': 'Не указан ID менеджера'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = OrderService.assign_order(
                order.id,
                manager_id,
                request.user
            )
            return Response(self.get_serializer(order).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Изменение статуса заявки.
        Доступно менеджерам и координаторам.
        """
        order = self.get_object()
        new_status = request.data.get('status')
        comment = request.data.get('comment', '')
        
        if not new_status:
            return Response(
                {'error': 'Не указан новый статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = OrderService.update_order_status(
                order.id,
                new_status,
                request.user,
                comment
            )
            return Response(self.get_serializer(order).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_to_blacklist(self, request, pk=None):
        """
        Добавление клиента в черный список.
        Требует координаторских прав.
        """
        order = self.get_object()
        reason = request.data.get('reason', '')
        
        if not reason:
            return Response(
                {'error': 'Не указана причина'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            blacklist_entry = OrderService.add_to_blacklist(
                order.id,
                reason
            )
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )