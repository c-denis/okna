from django.db import models
from .user import User
from .order import Order

class NotificationLog(models.Model):
    """
    Лог уведомлений, отправленных через Telegram.
    Позволяет отслеживать историю уведомлений.
    """
    NOTIFICATION_NEW = 'new'
    NOTIFICATION_ASSIGNED = 'assigned'
    NOTIFICATION_CANCELED = 'canceled'
    NOTIFICATION_COMPLETED = 'completed'
    
    NOTIFICATION_TYPES = [
        (NOTIFICATION_NEW, 'Новая заявка'),
        (NOTIFICATION_ASSIGNED, 'Назначение'),
        (NOTIFICATION_CANCELED, 'Отмена заявки'),
        (NOTIFICATION_COMPLETED, 'Завершение'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заявка')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель')
    message_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    message_text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')
    
    def __str__(self):
        return f"{self.get_message_type_display()} для {self.recipient}"
    
    class Meta:
        verbose_name = 'Лог уведомлений'
        verbose_name_plural = 'Логи уведомлений'
        ordering = ['-created_at']