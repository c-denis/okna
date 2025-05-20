from django.core.management.base import BaseCommand
from crm.services.notification_service import NotificationService
from crm.models import User, Order

class Command(BaseCommand):
    help = 'Отправка тестовых уведомлений менеджерам'

    def add_arguments(self, parser):
        parser.add_argument(
            '--manager',
            type=int,
            help='ID менеджера для отправки тестового уведомления'
        )

    def handle(self, *args, **options):
        manager_id = options['manager']
        
        if manager_id:
            # Отправка конкретному менеджеру
            try:
                manager = User.objects.get(id=manager_id, role__name='manager')
                self._send_test_notification(manager)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR('Менеджер не найден'))
        else:
            # Отправка всем менеджерам
            managers = User.objects.filter(role__name='manager')
            for manager in managers:
                self._send_test_notification(manager)

    def _send_test_notification(self, manager):
        """Вспомогательный метод для отправки уведомления"""
        if not manager.telegram_chat_id:
            self.stdout.write(
                self.style.WARNING(f'У менеджера {manager} не указан chat_id')
            )
            return
        
        # Создаем тестовую заявку
        test_order = Order.objects.create(
            client_name="Тестовый клиент",
            phone="+79990000000",
            address="Тестовый адрес",
            comment="Тестовая заявка для проверки уведомлений"
        )
        
        # Отправляем уведомление
        success = NotificationService.send_assignment_notification(test_order)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'Уведомление отправлено менеджеру {manager}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Ошибка отправки уведомления менеджеру {manager}')
            )
        
        # Удаляем тестовую заявку
        test_order.delete()