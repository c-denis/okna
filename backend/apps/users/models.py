from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Кастомная модель пользователя"""
    ROLE_CHOICES = [
        ('operator', 'Оператор'),
        ('coordinator', 'Координатор'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор')
    ]
    
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('busy', 'На заявке'),
        ('day_off', 'Выходной'),
        ('training', 'Обучение'),
        ('pair', 'В паре')
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='operator',
        verbose_name='Роль'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='free',
        verbose_name='Статус'
    )
    telegram_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Telegram ID'
    )
    current_order = models.OneToOneField(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_manager',
        verbose_name='Текущая заявка'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['telegram_id'],
                name='unique_telegram_id'
            )
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_available(self):
        return self.status == 'free' and not self.current_order

    def get_assigned_orders_count(self, date_range=None):
        qs = self.assigned_orders.all()
        if date_range:
            qs = qs.filter(created_at__range=date_range)
        return {
            'total': qs.count(),
            'completed': qs.filter(status='completed').count(),
            'rejected': qs.filter(status='rejected').count()
        }