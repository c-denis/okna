from django.dispatch import Signal

# Сигнал при добавлении в черный список
client_blacklisted = Signal()
"""
Аргументы:
- entry: BlacklistEntry - созданная запись
- order_id: int | None - ID связанной заявки
"""

# Сигнал при удалении из черного списка
client_unblocked = Signal()
"""
Аргументы:
- entry: BlacklistEntry - удаляемая запись
- order_ids: List[int] - IDs заявок, которые были разблокированы
"""

def handle_client_blacklisted(sender, **kwargs):
    """
    Обработчик сигнала - отправка уведомления о блокировке.
    """
    from ..tasks import send_blacklist_notification
    send_blacklist_notification.delay(
        kwargs['entry'].id,
        kwargs.get('order_id')
    )

def handle_client_unblocked(sender, **kwargs):
    """
    Обработчик сигнала - логирование разблокировки.
    """
    from ..models import SystemLog
    SystemLog.objects.create(
        action=f"Клиент {kwargs['entry'].client_name} разблокирован",
        details=f"Затронуто заявок: {len(kwargs['order_ids'])}"
    )

# Подключение сигналов
client_blacklisted.connect(handle_client_blacklisted)
client_unblocked.connect(handle_client_unblocked)