from django.template.loader import render_to_string
from .models import NotificationTemplate
from .services.notification_service import NotificationService

class NotificationBuilder:
    """
    Класс для построения сложных уведомлений с шаблонами.
    """
    
    @staticmethod
    def build_assignment_notification(order):
        """
        Создает уведомление о назначении заявки.
        """
        context = {
            'order': order,
            'manager': order.assigned_to,
            'client': order.client_name,
            'address': order.address
        }
        
        try:
            template = NotificationTemplate.objects.get(
                type='assignment',
                is_active=True
            )
            message = template.content.format(**context)
        except NotificationTemplate.DoesNotExist:
            message = render_to_string(
                'emails/assignment_notification.txt',
                context
            )
        
        return {
            'recipient': order.assigned_to,
            'message': message,
            'attachments': []
        }
    
    @staticmethod
    def build_status_change_notification(order, old_status):
        """
        Создает уведомление об изменении статуса.
        """
        context = {
            'order': order,
            'old_status': old_status,
            'new_status': order.get_status_display()
        }
        
        try:
            template = NotificationTemplate.objects.get(
                type='status_change',
                is_active=True
            )
            message = template.content.format(**context)
        except NotificationTemplate.DoesNotExist:
            message = render_to_string(
                'emails/status_change_notification.txt',
                context
            )
        
        recipients = [order.assigned_to] if order.assigned_to else []
        recipients += User.objects.filter(role__name='coordinator')
        
        return [{
            'recipient': recipient,
            'message': message,
            'attachments': []
        } for recipient in recipients]