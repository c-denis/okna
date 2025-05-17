from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .services.telegram_service import send_telegram_notification
import logging

logger = logging.getLogger(__name__)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def check_blacklist(self):
        if self.is_blacklisted:
            raise serializers.ValidationError("Клиент в черном списке!")


class Manager(models.Model):
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('busy', 'В работе'),
        ('day_off', 'Выходной'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free')
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_status_display()})"

    @property
    def active_requests(self):
        return self.request_set.filter(status='assigned').count()

    @property
    def rejected_today(self):
        from django.utils import timezone
        return self.request_set.filter(
            status='rejected',
            updated_at__date=timezone.now().date()
        ).count()


class Request(models.Model):
    STATUS_CHOICES = [
        ('unassigned', 'Не назначена'),
        ('assigned', 'Назначена'),
        ('in_progress', 'В работе'),
        ('completed', 'Исполнена'),
        ('rejected', 'Отказ'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unassigned')
    manager = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id} ({self.client.name})"


@receiver(post_save, sender=Request)
def notify_telegram(sender, instance, created, **kwargs):
    try:
        if created or instance.status == 'assigned':
            message = (
                f"<b>🆕 Новая заявка #{instance.id}</b>\n"
                f"👤 <b>Клиент:</b> {instance.client.name}\n"
                f"📞 <b>Телефон:</b> {instance.client.phone}\n"
                f"📍 <b>Адрес:</b> {instance.city.name}, {instance.address}\n"
                f"🛠 <b>Статус:</b> {instance.get_status_display()}"
            )
            send_telegram_notification(message)
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {str(e)}")