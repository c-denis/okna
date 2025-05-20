"""
Инициализация ViewSets API v1.
"""
from .order import OrderViewSet
from .user import UserViewSet
from .location import LocationViewSet
from .blacklist import BlacklistViewSet
from .manager_status import ManagerStatusViewSet
from .reports import OrderReportViewSet, ManagerReportViewSet

__all__ = [
    'OrderViewSet', 'UserViewSet', 'LocationViewSet',
    'BlacklistViewSet', 'ManagerStatusViewSet',
    'OrderReportViewSet', 'ManagerReportViewSet'
]