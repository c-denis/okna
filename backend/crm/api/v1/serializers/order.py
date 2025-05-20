from rest_framework import serializers
from ...models import Order, StatusHistory
from .user import UserSerializer
from .location import AddressSerializer

class StatusHistorySerializer(serializers.ModelSerializer):
    """
    Сериализатор истории изменения статусов заявки.
    """
    changed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = StatusHistory
        fields = ['status', 'changed_by', 'changed_at', 'comment']
        read_only_fields = fields

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявок с поддержкой:
    - Детальной информации о заявке
    - Связанных объектов (адрес, менеджер)
    - Истории изменений статусов
    """
    address = AddressSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'client_name', 'phone', 'address', 'comment',
            'status', 'created_at', 'assigned_to', 'is_blacklisted',
            'status_history'
        ]
        read_only_fields = ['id', 'created_at', 'status_history', 'is_blacklisted']
    
    def validate(self, data):
        """
        Валидация данных заявки:
        - Проверка формата телефона
        - Проверка статусов при изменении
        """
        if 'phone' in data:
            validator = PhoneValidator()
            data['phone'] = validator(data['phone'])
        
        # Дополнительные проверки при изменении статуса
        if 'status' in data:
            current_status = self.instance.status if self.instance else None
            new_status = data['status']
            
            # Логика проверки допустимых переходов статусов
            if current_status == 'completed' and new_status != 'completed':
                raise serializers.ValidationError(
                    "Завершенную заявку нельзя изменить"
                )
        
        return data
    
    def create(self, validated_data):
        """
        Создание новой заявки через API.
        Использует OrderService для соблюдения бизнес-логики.
        """
        from ...services.order_service import OrderService
        
        return OrderService.create_order(
            client_name=validated_data['client_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            comment=validated_data.get('comment', ''),
            operator=self.context['request'].user
        )