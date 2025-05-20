from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import BlacklistEntry, Order
from .serializers.blacklist import (
    BlacklistEntrySerializer,
    AddToBlacklistSerializer
)
from ...permissions import IsCoordinatorOrHigher
from ...services.blacklist_service import BlacklistService

class BlacklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с черным списком клиентов.
    Доступен только координаторам и администраторам.
    """
    queryset = BlacklistEntry.objects.all().order_by('-created_at')
    serializer_class = BlacklistEntrySerializer
    permission_classes = [IsCoordinatorOrHigher]

    @action(
        detail=True,
        methods=['post'],
        serializer_class=serializers.Serializer
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
            BlacklistEntrySerializer(entry).data,
            status=status.HTTP_201_CREATED
        )

class OrderBlacklistView(viewsets.GenericViewSet):
    """
    Отдельный ViewSet для черного списка в контексте заявки.
    """
    permission_classes = [IsCoordinatorOrHigher]

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
            BlacklistEntrySerializer(entry).data,
            status=status.HTTP_201_CREATED
        )