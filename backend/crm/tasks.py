# crm/tasks.py
from config.celery import shared_task
from .models import Order
from .services.notification_service import NotificationService

@shared_task
def check_pending_orders():
    """Периодическая проверка необработанных заявок"""
    pending_orders = Order.objects.filter(status='pending')
    for order in pending_orders:
        NotificationService.send_pending_notification(order)
    return f"Checked {pending_orders.count()} pending orders"