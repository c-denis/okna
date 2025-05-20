from django.test import TestCase
from crm.models import Order, User

class OrderModelTest(TestCase):
    def test_order_creation(self):
        """Тест создания модели заявки"""
        order = Order.objects.create(
            client_name="Тестовый клиент",
            phone="+79990000000",
            address="Тестовый адрес"
        )
        self.assertEqual(str(order), f"Заявка #{order.id} - Тестовый клиент")
        self.assertEqual(order.status, 'unassigned')