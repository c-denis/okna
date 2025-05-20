from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import Order, City

class ReportService:
    """
    Сервис для генерации отчетов по заявкам.
    Поддерживает все варианты отчетов из ТЗ:
    - По локациям (городам)
    - По статусам
    - За различные периоды
    """
    
    PERIODS = {
        'today': 'Сегодня',
        'yesterday': 'Вчера',
        'week': 'Текущая неделя',
        'last_week': 'Прошлая неделя',
        'month': 'Текущий месяц',
        'last_month': 'Прошлый месяц',
        'custom': 'Произвольный период'
    }
    
    @classmethod
    def get_orders_report(cls, period='today', date_from=None, date_to=None):
        """
        Генерация сводного отчета по заявкам.
        
        Args:
            period (str): Период из PERIODS
            date_from (date): Начальная дата (для произвольного периода)
            date_to (date): Конечная дата (для произвольного периода)
            
        Returns:
            dict: Данные отчета
        """
        # Определяем временной диапазон
        date_range = cls._get_date_range(period, date_from, date_to)
        
        # Базовый запрос
        orders = Order.objects.filter(created_at__range=date_range)
        
        # Группировка по городам
        by_city = orders.values('address__city__name').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            rejected=Count('id', filter=Q(status='rejected')),
            in_progress=Count('id', filter=Q(status='in_progress'))
        ).order_by('-total')
        
        # Общая статистика
        total_stats = {
            'total': orders.count(),
            'completed': orders.filter(status='completed').count(),
            'rejected': orders.filter(status='rejected').count(),
            'in_progress': orders.filter(status='in_progress').count(),
            'unassigned': orders.filter(status='unassigned').count()
        }
        
        return {
            'period': cls.PERIODS[period],
            'date_from': date_range[0],
            'date_to': date_range[1],
            'by_city': list(by_city),
            'total_stats': total_stats
        }
    
    @classmethod
    def get_managers_report(cls, period='today', date_from=None, date_to=None):
        """
        Отчет по эффективности менеджеров.
        
        Args:
            period (str): Период из PERIODS
            date_from (date): Начальная дата
            date_to (date): Конечная дата
            
        Returns:
            dict: Данные отчета
        """
        date_range = cls._get_date_range(period, date_from, date_to)
        
        # Статистика по менеджерам
        managers_stats = Order.objects.filter(
            created_at__range=date_range,
            assigned_to__isnull=False
        ).values('assigned_to__username', 'assigned_to__first_name', 'assigned_to__last_name').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            rejected=Count('id', filter=Q(status='rejected')),
            avg_time=Avg(
                Case(
                    When(status='completed', then=F('completed_at') - F('started_at')),
                    output_field=DurationField()
                )
            )
        ).order_by('-completed')
        
        return {
            'period': cls.PERIODS[period],
            'date_from': date_range[0],
            'date_to': date_range[1],
            'managers': list(managers_stats)
        }
    
    @staticmethod
    def _get_date_range(period, date_from, date_to):
        """
        Вычисляет диапазон дат для отчетов.
        
        Args:
            period (str): Ключ периода
            date_from (date): Начальная дата
            date_to (date): Конечная дата
            
        Returns:
            tuple: (date_from, date_to)
        """
        today = timezone.now().date()
        
        if period == 'today':
            return (today, today + timedelta(days=1))
        elif period == 'yesterday':
            return (today - timedelta(days=1), today)
        elif period == 'week':
            start = today - timedelta(days=today.weekday())
            return (start, start + timedelta(days=7))
        elif period == 'last_week':
            start = today - timedelta(days=today.weekday() + 7)
            return (start, start + timedelta(days=7))
        elif period == 'month':
            return (today.replace(day=1), today.replace(day=1) + timedelta(days=32)).replace(day=1))
        elif period == 'last_month':
            first = today.replace(day=1) - timedelta(days=1)
            return (first.replace(day=1), today.replace(day=1))
        elif period == 'custom' and date_from and date_to:
            return (date_from, date_to)
        else:
            return (today - timedelta(days=30), today)