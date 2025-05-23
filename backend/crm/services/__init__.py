"""
Инициализация сервисного слоя.
Экспортирует основные сервисы для удобного импорта в других модулях.
"""
from .order_service import OrderService
from .notification_service import NotificationService
from .report_service import ReportService
from .validator import PhoneValidator, AddressValidator
# from .fias_integration import FIASIntegration

__all__ = [
    'OrderService',
    'NotificationService',
    'ReportService',
    'PhoneValidator',
    'AddressValidator',
    'FIASIntegration'
]