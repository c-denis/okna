from rest_framework import viewsets, permissions
from rest_framework.response import Response
from crm.services.report_service import ReportService

class OrderReportViewSet(viewsets.ViewSet):
    """
    ViewSet для генерации отчетов по заявкам.
    Доступен только координаторам и администраторам.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """
        Генерация сводного отчета по заявкам.
        Поддерживает фильтрацию по периодам.
        """
        if not (request.user.is_coordinator or request.user.is_superuser):
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        period = request.query_params.get('period', 'today')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        report = ReportService.get_orders_report(period, date_from, date_to)
        return Response(report)

class ManagerReportViewSet(viewsets.ViewSet):
    """
    ViewSet для генерации отчетов по менеджерам.
    Показывает эффективность работы менеджеров.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """
        Генерация отчета по менеджерам.
        """
        if not (request.user.is_coordinator or request.user.is_superuser):
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        period = request.query_params.get('period', 'today')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        report = ReportService.get_managers_report(period, date_from, date_to)
        return Response(report)