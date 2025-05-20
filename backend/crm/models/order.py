from django.db import models
from django.utils import timezone
from .user import User
from .location import Address

class Order(models.Model):
    """
    Модель заявки на ремонтные услуги.
    Соответствует основному бизнес-процессу из ТЗ.
    """
    # Варианты статусов заявки (константы для избежания "магических строк")
    STATUS_UNASSIGNED = 'unassigned'
    STATUS_ASSIGNED = 'assigned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_UNASSIGNED, 'Не назначена'),
        (STATUS_ASSIGNED, 'Назначена'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_COMPLETED, 'Исполнена'),
        (STATUS_REJECTED, 'Отказ'),
    ]
    
    # Основные поля заявки
    client_name = models.CharField(max_length=100, verbose_name='ФИО клиента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='Адрес')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_UNASSIGNED,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    assigned_to = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Назначенный менеджер'
    )
    is_blacklisted = models.BooleanField(default=False, verbose_name='Черный список')
    
    # Методы модели
    def __str__(self):
        return f"Заявка #{self.id} - {self.client_name}"
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

class StatusHistory(models.Model):
    """
    История изменения статусов заявки.
    Позволяет отслеживать все изменения статусов с временными метками.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.order.id}: {self.get_status_display()} ({self.changed_at})"
    
    class Meta:
        verbose_name = 'История статуса'
        verbose_name_plural = 'История статусов'