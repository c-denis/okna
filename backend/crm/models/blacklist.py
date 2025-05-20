from django.db import models
from .order import Order

class BlacklistEntry(models.Model):
    """
    Модель записи в черном списке.
    Связана с заявками через ManyToMany.
    """
    client_name = models.CharField(
        max_length=100,
        verbose_name="ФИО клиента"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )
    reason = models.TextField(
        verbose_name="Причина блокировки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    related_orders = models.ManyToManyField(
        Order,
        verbose_name="Связанные заявки",
        blank=True
    )

    class Meta:
        verbose_name = "Запись черного списка"
        verbose_name_plural = "Черный список клиентов"
        unique_together = [['client_name', 'phone']]

    def __str__(self):
        return f"{self.client_name} ({self.phone})"