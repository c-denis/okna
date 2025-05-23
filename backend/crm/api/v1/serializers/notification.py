from rest_framework import serializers
from crm.models import NotificationLog
from .user import UserSerializer
from .order import OrderSerializer

class NotificationLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор лога уведомлений.
    Отображает полную информацию об отправленных уведомлениях.
    """
    order = OrderSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'order', 'recipient', 'message_type',
            'message_text', 'created_at', 'is_sent'
        ]
        read_only_fields = fields