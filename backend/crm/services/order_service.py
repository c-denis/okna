from django.utils import timezone
from ..models import Order, StatusHistory, Blacklist, User
from .notification_service import NotificationService

class OrderService:
    """
    Сервис для работы с заявками (бизнес-логика).
    Реализует основные операции согласно ТЗ:
    - Создание/редактирование заявок
    - Назначение менеджеров
    - Изменение статусов
    - Работа с черным списком
    """
    
    @staticmethod
    def create_order(client_name, phone, address, comment, operator):
        """
        Создание новой заявки.
        Проверяет клиента на наличие в черном списке.
        
        Args:
            client_name (str): ФИО клиента
            phone (str): Номер телефона
            address (Address): Объект адреса
            comment (str): Комментарий к заявке
            operator (User): Оператор, создавший заявку
            
        Returns:
            Order: Созданный объект заявки
        """
        # Проверка на черный список
        is_blacklisted = Blacklist.objects.filter(
            client_name=client_name,
            phone=phone
        ).exists()
        
        order = Order.objects.create(
            client_name=client_name,
            phone=phone,
            address=address,
            comment=comment,
            is_blacklisted=is_blacklisted,
            assigned_to=None
        )
        
        # Запись в историю статусов
        StatusHistory.objects.create(
            order=order,
            status=Order.STATUS_UNASSIGNED,
            changed_by=operator,
            comment='Заявка создана'
        )
        
        return order
    
    @staticmethod
    def assign_order(order_id, manager_id, coordinator):
        """
        Назначение заявки менеджеру.
        Проверяет, что менеджер свободен.
        
        Args:
            order_id (int): ID заявки
            manager_id (int): ID менеджера
            coordinator (User): Координатор, выполняющий назначение
            
        Returns:
            Order: Обновленный объект заявки
        """
        order = Order.objects.get(id=order_id)
        manager = User.objects.get(id=manager_id)
        
        # Проверка статуса менеджера
        if hasattr(manager, 'managerstatus') and manager.managerstatus.status != 'free':
            raise ValueError('Менеджер уже занят другой заявкой')
        
        # Обновление заявки
        order.assigned_to = manager
        order.status = Order.STATUS_ASSIGNED
        order.save()
        
        # Обновление статуса менеджера
        if hasattr(manager, 'managerstatus'):
            manager.managerstatus.status = 'busy'
            manager.managerstatus.save()
        
        # Запись в историю
        StatusHistory.objects.create(
            order=order,
            status=Order.STATUS_ASSIGNED,
            changed_by=coordinator,
            comment=f'Назначен менеджер: {manager.get_full_name()}'
        )
        
        # Отправка уведомления
        NotificationService.send_assignment_notification(order)
        
        return order
    
    @staticmethod
    def update_order_status(order_id, new_status, user, comment=''):
        """
        Изменение статуса заявки с записью в историю.
        
        Args:
            order_id (int): ID заявки
            new_status (str): Новый статус из Order.STATUS_CHOICES
            user (User): Пользователь, изменивший статус
            comment (str): Комментарий к изменению
            
        Returns:
            Order: Обновленный объект заявки
        """
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        
        # Если заявка завершена/отклонена, освобождаем менеджера
        if new_status in [Order.STATUS_COMPLETED, Order.STATUS_REJECTED]:
            if order.assigned_to and hasattr(order.assigned_to, 'managerstatus'):
                order.assigned_to.managerstatus.status = 'free'
                order.assigned_to.managerstatus.save()
        
        # Запись в историю
        StatusHistory.objects.create(
            order=order,
            status=new_status,
            changed_by=user,
            comment=comment
        )
        
        # Отправка уведомления при завершении
        if new_status == Order.STATUS_COMPLETED:
            NotificationService.send_completion_notification(order)
        
        return order
    
    @staticmethod
    def add_to_blacklist(order_id, reason):
        """
        Добавление клиента в черный список на основе заявки.
        
        Args:
            order_id (int): ID заявки
            reason (str): Причина добавления
            
        Returns:
            Blacklist: Созданная запись в черном списке
        """
        order = Order.objects.get(id=order_id)
        
        blacklist_entry, created = Blacklist.objects.get_or_create(
            client_name=order.client_name,
            phone=order.phone,
            defaults={'reason': reason}
        )
        
        if not created:
            blacklist_entry.reason = reason
            blacklist_entry.save()
        
        # Обновляем связанные заявки
        blacklist_entry.related_orders.add(order)
        Order.objects.filter(client_name=order.client_name, phone=order.phone).update(is_blacklisted=True)
        
        return blacklist_entry