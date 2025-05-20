import telegram
from django.conf import settings
from django.utils import timezone
from ..models import NotificationLog

class NotificationService:
    """
    Сервис для отправки уведомлений через Telegram.
    Интегрируется с Telegram Bot API и логирует все отправленные уведомления.
    """
    
    _bot = None
    
    @classmethod
    def initialize_bot(cls):
        """Инициализация бота при старте приложения"""
        if not cls._bot and hasattr(settings, 'TELEGRAM_BOT_TOKEN'):
            cls._bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    @classmethod
    def _send_telegram_message(cls, chat_id, message):
        """
        Внутренний метод для отправки сообщения через Telegram API.
        
        Args:
            chat_id (str): ID чата или группы
            message (str): Текст сообщения
            
        Returns:
            bool: Успешно ли отправлено сообщение
        """
        if not cls._bot:
            cls.initialize_bot()
        
        try:
            cls._bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки Telegram сообщения: {e}")
            return False
    
    @classmethod
    def send_assignment_notification(cls, order):
        """
        Уведомление о назначении заявки менеджеру.
        
        Args:
            order (Order): Объект заявки
        """
        if not order.assigned_to or not order.assigned_to.telegram_chat_id:
            return
        
        message = (
            f"<b>Новая заявка №{order.id}</b>\n"
            f"Клиент: {order.client_name}\n"
            f"Адрес: {order.address}\n"
            f"Телефон: {order.phone}\n"
            f"Статус: Назначена"
        )
        
        success = cls._send_telegram_message(
            order.assigned_to.telegram_chat_id,
            message
        )
        
        # Логирование уведомления
        NotificationLog.objects.create(
            order=order,
            recipient=order.assigned_to,
            message_type='assigned',
            message_text=message,
            is_sent=success
        )
    
    @classmethod
    def send_completion_notification(cls, order):
        """
        Уведомление о завершении заявки (координатору).
        
        Args:
            order (Order): Объект заявки
        """
        # Находим координаторов
        coordinators = User.objects.filter(role__name='coordinator', telegram_chat_id__isnull=False)
        
        message = (
            f"<b>Заявка №{order.id} завершена</b>\n"
            f"Клиент: {order.client_name}\n"
            f"Менеджер: {order.assigned_to.get_full_name() if order.assigned_to else 'Не назначен'}\n"
            f"Статус: {order.get_status_display()}"
        )
        
        for coordinator in coordinators:
            success = cls._send_telegram_message(
                coordinator.telegram_chat_id,
                message
            )
            
            NotificationLog.objects.create(
                order=order,
                recipient=coordinator,
                message_type='completed',
                message_text=message,
                is_sent=success
            )
    
    @classmethod
    def send_cancellation_notification(cls, order, reason):
        """
        Уведомление об отмене заявки.
        
        Args:
            order (Order): Объект заявки
            reason (str): Причина отмены
        """
        recipients = []
        
        if order.assigned_to:
            recipients.append(order.assigned_to)
        
        # Добавляем координаторов
        recipients.extend(User.objects.filter(role__name='coordinator', telegram_chat_id__isnull=False))
        
        message = (
            f"<b>Заявка №{order.id} отменена</b>\n"
            f"Причина: {reason}\n"
            f"Клиент: {order.client_name}\n"
            f"Адрес: {order.address}"
        )
        
        for recipient in recipients:
            if not recipient.telegram_chat_id:
                continue
                
            success = cls._send_telegram_message(
                recipient.telegram_chat_id,
                message
            )
            
            NotificationLog.objects.create(
                order=order,
                recipient=recipient,
                message_type='canceled',
                message_text=message,
                is_sent=success
            )