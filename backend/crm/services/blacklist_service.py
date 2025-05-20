from ..models import BlacklistEntry, Order
from ..signals import client_blacklisted, client_unblocked

class BlacklistService:
    """
    Сервис для бизнес-логики работы с черным списком.
    Инкапсулирует основную логику и обработку сигналов.
    """
    
    def add_to_blacklist(self, client_name, phone, reason, order_id=None):
        """
        Основной метод добавления в черный список.
        1. Создает или обновляет запись в ЧС
        2. Помечает связанные заявки
        3. Отправляет сигналы
        """
        entry, created = BlacklistEntry.objects.update_or_create(
            client_name=client_name,
            phone=phone,
            defaults={'reason': reason}
        )

        # Обновляем связанные заявки
        if order_id:
            order = Order.objects.get(id=order_id)
            entry.related_orders.add(order)
            order.is_blacklisted = True
            order.save()

        # Помечаем все заявки этого клиента
        Order.objects.filter(
            client_name=client_name,
            phone=phone
        ).update(is_blacklisted=True)

        # Отправка сигнала
        client_blacklisted.send(
            sender=self.__class__,
            entry=entry,
            order_id=order_id
        )

        return entry

    def remove_from_blacklist(self, entry_id):
        """
        Удаление из черного списка с очисткой флагов у заявок.
        """
        entry = BlacklistEntry.objects.get(id=entry_id)
        orders = entry.related_orders.all()
        
        # Снимаем флаги
        Order.objects.filter(
            client_name=entry.client_name,
            phone=entry.phone
        ).update(is_blacklisted=False)
        
        # Отправка сигнала перед удалением
        client_unblocked.send(
            sender=self.__class__,
            entry=entry,
            order_ids=list(orders.values_list('id', flat=True))
        )
        
        entry.delete()