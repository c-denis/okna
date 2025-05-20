from rest_framework import viewsets, permissions
from ...models import City, Address
from ..serializers import CitySerializer, AddressSerializer
from ...services.fias_integration import FIASIntegration

class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с локациями (города и адреса).
    Поддерживает поиск через ФИАС API.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Поиск городов по названию.
        Использует ФИАС API или локальную базу.
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Не указан поисковый запрос'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = FIASIntegration.search_city(query)
        return Response(results)