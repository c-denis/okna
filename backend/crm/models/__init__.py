# Импорт всех моделей для удобного доступа из других модулей
from .user import User, Role, ManagerStatus
from .order import Order, StatusHistory
from .location import City, Address
from .blacklist import Blacklist
from .notification import NotificationLog

# Делаем модели доступными при импорте из models
__all__ = [
    'User', 'Role', 'ManagerStatus',
    'Order', 'StatusHistory',
    'City', 'Address',
    'Blacklist',
    'NotificationLog'
]