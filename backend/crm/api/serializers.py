from rest_framework import serializers
from .models import City, Client, Manager, Request

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

        def validate(self, data):
            client = data.get('client')
            if client and client.is_blacklisted:
                raise serializers.ValidationError("Клиент в черном списке!")
            return data

