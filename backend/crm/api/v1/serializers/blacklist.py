from rest_framework import serializers
from ...models import BlacklistEntry, Order
from ...services.blacklist_service import BlacklistService

class BlacklistEntrySerializer(serializers.ModelSerializer):
    """
    Сериализатор для записей черного списка.
    Включает все поля модели и дополнительные computed-поля.
    """
    related_orders_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlacklistEntry
        fields = [
            'id',
            'client_name',
            'phone',
            'reason',
            'created_at',
            'related_orders_count'
        ]
        read_only_fields = ['created_at']

    def get_related_orders_count(self, obj):
        """Количество связанных заявок клиента."""
        return obj.related_orders.count()

class AddToBlacklistSerializer(serializers.Serializer):
    """
    Сериализатор для добавления в черный список.
    Валидирует входные данные и обрабатывает логику добавления.
    """
    reason = serializers.CharField(
        max_length=500,
        required=True,
        help_text="Причина добавления в черный список"
    )
    order_id = serializers.IntegerField(
        required=False,
        help_text="ID заявки, связанной с блокировкой"
    )

    def validate(self, attrs):
        """Дополнительная валидация данных."""
        if 'order_id' in attrs:
            try:
                order = Order.objects.get(id=attrs['order_id'])
                attrs['client_name'] = order.client_name
                attrs['phone'] = order.phone
            except Order.DoesNotExist:
                raise serializers.ValidationError(
                    {"order_id": "Заявка не найдена"}
                )
        return attrs

    def create(self, validated_data):
        """Создание записи в черном списке."""
        service = BlacklistService()
        return service.add_to_blacklist(
            client_name=validated_data['client_name'],
            phone=validated_data['phone'],
            reason=validated_data['reason'],
            order_id=validated_data.get('order_id')
        )