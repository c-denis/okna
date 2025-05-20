from rest_framework import serializers
from ...models import City, Address

class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор городов с поддержкой ФИАС.
    """
    class Meta:
        model = City
        fields = ['id', 'name', 'fias_id']
        read_only_fields = ['fias_id']

class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор адресов с детализацией:
    - Город (вложенный сериализатор)
    - Полный адрес в строковом представлении
    """
    city = CitySerializer(read_only=True)
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Address
        fields = [
            'id', 'city', 'street', 'house', 
            'building', 'apartment', 'full_address'
        ]
    
    def get_full_address(self, obj):
        """
        Формирует полный адрес в формате:
        "Город, улица, дом, корпус, квартира"
        """
        parts = [obj.city.name, f"ул. {obj.street}", f"д. {obj.house}"]
        if obj.building:
            parts.append(f"к. {obj.building}")
        if obj.apartment:
            parts.append(f"кв. {obj.apartment}")
        return ", ".join(parts)
    
    def validate(self, data):
        """
        Валидация адреса:
        - Проверка обязательных полей
        - Нормализация данных
        """
        from ...services.validator import AddressValidator
        validator = AddressValidator()
        validator.validate_address(data)
        return data