from rest_framework import viewsets, status, serializers  # Добавлен импорт serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from crm.models import Blacklist, Order
from ..serializers.blacklist import (
    BlacklistSerializer,
    AddToBlacklistSerializer
)
from ..permissions import IsCoordinator
from crm.services.blacklist_service import BlacklistService  # Исправлен относительный импорт

class BlacklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с черным списком клиентов.
    Доступен только координаторам и администраторам.
    """
    queryset = Blacklist.objects.all().order_by('-created_at')
    serializer_class = BlacklistSerializer
    permission_classes = [IsCoordinator]

    @action(
        detail=True,
        methods=['post'],
        serializer_class=serializers.Serializer  # Теперь serializers импортирован
    )
    def unblock(self, request, pk=None):
        """
        Разблокировка клиента (удаление из черного списка).
        Также снимает флаги is_blacklisted с связанных заявок.
        """
        entry = self.get_object()
        service = BlacklistService()
        service.remove_from_blacklist(entry.id)
        return Response(
            {"status": "Клиент удален из черного списка"},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        serializer_class=AddToBlacklistSerializer
    )
    def add_from_order(self, request):
        """
        Специальный endpoint для добавления в ЧС из заявки.
        Принимает order_id и reason.
        """
        serializer = AddToBlacklistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        entry = serializer.save()
        return Response(
            BlacklistSerializer(entry).data,
            status=status.HTTP_201_CREATED
        )

class OrderBlacklistView(viewsets.GenericViewSet):
    """
    Отдельный ViewSet для черного списка в контексте заявки.
    """
    queryset = Order.objects.all()  # Добавлен queryset
    permission_classes = [IsCoordinator]

    @action(
        detail=True,
        methods=['post'],
        serializer_class=AddToBlacklistSerializer
    )
    def blacklist(self, request, pk=None):
        """
        Добавляет клиента из заявки в черный список.
        """
        order = self.get_object()
        serializer = AddToBlacklistSerializer(data={
            **request.data,
            'order_id': order.id
        })
        serializer.is_valid(raise_exception=True)
        
        entry = serializer.save()
        return Response(
            BlacklistSerializer(entry).data,
            status=status.HTTP_201_CREATED
        )