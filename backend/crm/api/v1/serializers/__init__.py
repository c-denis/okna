"""
Инициализация сериализаторов API v1.
"""
from .order import OrderSerializer, StatusHistorySerializer
from .user import UserSerializer, ManagerStatusSerializer
from .location import CitySerializer, AddressSerializer
from .blacklist import BlacklistSerializer
from .notification import NotificationLogSerializer

__all__ = [
    'OrderSerializer', 'StatusHistorySerializer',
    'UserSerializer', 'ManagerStatusSerializer',
    'CitySerializer', 'AddressSerializer',
    'BlacklistSerializer',
    'NotificationLogSerializer'
]