from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import City, Client, Manager, Request
from .serializers import CitySerializer, ClientSerializer, ManagerSerializer, RequestSerializer
import json
import logging

logger = logging.getLogger(__name__)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Назначение заявки менеджеру"""
        instance = self.get_object()
        manager_id = request.data.get('manager_id')

        try:
            manager = Manager.objects.get(id=manager_id)
            instance.manager = manager
            instance.status = 'assigned'
            instance.save()
            return Response({'status': 'success'})
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            callback_query = data.get('callback_query', {})
            callback_data = callback_query.get('data', '')
            chat_id = callback_query['message']['chat']['id']

            if callback_data == 'accept_request':
                # Логика принятия заявки
                return JsonResponse({'status': 'accepted'})
            elif callback_data == 'reject_request':
                # Логика отклонения заявки
                return JsonResponse({'status': 'rejected'})

        except Exception as e:
            logger.error(f"Telegram webhook error: {e}")
            return JsonResponse({'status': 'error'}, status=500)
    return JsonResponse({'status': 'invalid method'}, status=405)

from django.db.models import Count, Q

@action(detail=False, methods=['get'])
def manager_stats(self, request):
    from django.db.models import Count, Q
    stats = Manager.objects.annotate(
        completed=Count('request', filter=Q(request__status='completed')),
        rejected=Count('request', filter=Q(request__status='rejected')),
    ).values('user__username', 'completed', 'rejected')
    return Response(stats)