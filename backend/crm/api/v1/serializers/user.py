from rest_framework import serializers
from django.contrib.auth.models import Group
from crm.models import User, ManagerStatus

class ManagerStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор статусов менеджеров.
    """
    class Meta:
        model = ManagerStatus
        fields = ['status', 'last_updated']
        read_only_fields = ['last_updated']

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей с поддержкой:
    - Основных данных пользователя
    - Статуса менеджера (если есть)
    - Групп и прав
    """
    manager_status = ManagerStatusSerializer(read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'telegram_chat_id', 'manager_status', 'groups'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'telegram_chat_id': {'required': False}
        }
    
    def create(self, validated_data):
        """
        Создание пользователя с хешированием пароля.
        """
        groups = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user
    
    def update(self, instance, validated_data):
        """
        Обновление пользователя с обработкой пароля.
        """
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        if groups is not None:
            instance.groups.set(groups)
        
        return instance