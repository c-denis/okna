from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from crm.models import Order

User = get_user_model()

class OrderFlowIntegrationTest(TestCase):
    """Интеграционные тесты workflow заявок"""
    
    def setUp(self):
        self.client = APIClient()
        self.operator = User.objects.create_user(
            username='operator',
            password='testpass123',
            role='operator'
        )
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            role='manager'
        )
        
    def test_order_full_cycle(self):
        """Тест полного цикла заявки: создание -> назначение -> выполнение"""
        # Аутентификация оператора
        self.client.force_authenticate(user=self.operator)
        
        # 1. Создание заявки
        create_url = reverse('order-list')
        response = self.client.post(create_url, {
            'client_name': 'Петров Петр',
            'phone': '+79998887766',
            'address': 'ул. Примерная, д.10'
        })
        self.assertEqual(response.status_code, 201)
        
        # 2. Назначение заявки менеджеру (координатором)
        self.coordinator = User.objects.create_user(
            username='coordinator',
            password='testpass123',
            role='coordinator'
        )
        self.client.force_authenticate(user=self.coordinator)
        
        order_id = response.data['id']
        assign_url = reverse('order-assign', kwargs={'pk': order_id})
        response = self.client.post(assign_url, {
            'manager_id': self.manager.id
        })
        self.assertEqual(response.status_code, 200)
        
        # 3. Менеджер отмечает выполнение
        self.client.force_authenticate(user=self.manager)
        complete_url = reverse('order-update-status', kwargs={'pk': order_id})
        response = self.client.post(complete_url, {
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 200)