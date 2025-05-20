"""
Инициализация API модуля.
Экспортирует основные компоненты API для удобного доступа.
"""
from .v1.serializers import *
from .v1.views import *

__all__ = [
    # Сериализаторы
    'OrderSerializer', 'UserSerializer', 'LocationSerializer',
    'BlacklistSerializer', 'ManagerStatusSerializer',
    
    # ViewSets
    'OrderViewSet', 'UserViewSet', 'LocationViewSet',
    'BlacklistViewSet', 'ManagerStatusViewSet',
    
    # Другие компоненты
    'api_v1_router'
]