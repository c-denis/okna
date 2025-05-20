from django.test import TestCase
from django.contrib.auth import get_user_model
from crm.services.order_service import OrderService
from crm.models import Order

User = get_user_model()

class OrderServiceTestCase(TestCase):
    """Тестирование сервиса работы с заявками"""
    
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя (оператора)
        cls.operator = User.objects.create_user(
            username='operator',
            password='testpass123',
            role='operator'
        )
        
    def test_create_order(self):
        """Тест создания заявки"""
        order = OrderService.create_order(
            client_name="Иванов Иван",
            phone="+79991234567",
            address="ул. Тестовая, д.1",
            comment="Тестовая заявка",
            operator=self.operator
        )
        
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.client_name, "Иванов Иван")
        self.assertEqual(order.status, 'unassigned')