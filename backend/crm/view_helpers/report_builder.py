from django.db.models import Count, Q, F
from datetime import datetime, timedelta
from .models import Order, User

class ReportBuilder:
    """
    Класс для построения сложных отчетов с возможностью фильтрации.
    """
    
    def __init__(self, request):
        self.request = request
        self.base_queryset = Order.objects.all()
    
    def build_manager_report(self):
        """
        Отчет по эффективности менеджеров.
        """
        period = self._get_period()
        queryset = self.base_queryset.filter(
            created_at__range=(period['start'], period['end'])
        )
        
        return queryset.values(
            'assigned_to__username',
            'assigned_to__first_name',
            'assigned_to__last_name'
        ).annotate(
            total_orders=Count('id'),
            completed_orders=Count('id', filter=Q(status='completed')),
            rejected_orders=Count('id', filter=Q(status='rejected')),
            completion_rate=F('completed_orders') * 100 / F('total_orders')
        ).order_by('-completion_rate')
    
    def build_location_report(self):
        """
        Отчет по заявкам в разрезе локаций.
        """
        period = self._get_period()
        queryset = self.base_queryset.filter(
            created_at__range=(period['start'], period['end'])
        )
        
        return queryset.values(
            'address__city__name',
            'address__street'
        ).annotate(
            total_orders=Count('id'),
            in_progress=Count('id', filter=Q(status='in_progress')),
            completed=Count('id', filter=Q(status='completed')),
            rejected=Count('id', filter=Q(status='rejected'))
        ).order_by('-total_orders')
    
    def _get_period(self):
        """
        Определяет период для отчетов на основе параметров запроса.
        """
        period_type = self.request.GET.get('period', 'week')
        
        today = datetime.now().date()
        
        if period_type == 'today':
            return {'start': today, 'end': today + timedelta(days=1)}
        elif period_type == 'week':
            return {'start': today - timedelta(days=7), 'end': today}
        elif period_type == 'month':
            return {'start': today - timedelta(days=30), 'end': today}
        else:
            # Пользовательский период
            start = self.request.GET.get('start_date', today - timedelta(days=7))
            end = self.request.GET.get('end_date', today)
            return {'start': start, 'end': end}