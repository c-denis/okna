from django.db import models
from django.core.validators import MinLengthValidator
from apps.users.models import User

class Location(models.Model):
    """Модель локации (города)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название города'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """Основная модель заявки"""
    STATUS_CHOICES = [
        ('unassigned', 'Не назначена'),
        ('assigned', 'Назначена'),
        ('in_progress', 'В работе'),
        ('completed', 'Исполнена'),
        ('rejected', 'Отказ')
    ]

    client_name = models.CharField(
        max_length=200,
        verbose_name='ФИО клиента',
        validators=[MinLengthValidator(3)]
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    address = models.TextField(
        verbose_name='Полный адрес'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        verbose_name='Город'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unassigned',
        verbose_name='Статус'
    )
    operator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_orders',
        verbose_name='Оператор'
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_orders',
        null=True,
        blank=True,
        verbose_name='Менеджер'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время начала работ'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время завершения'
    )
    is_blacklisted = models.BooleanField(
        default=False,
        verbose_name='Черный список'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Заявка #{self.id} - {self.client_name}'

    @property
    def full_address(self):
        return f"{self.location}, {self.address}"