import openpyxl
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from .models import Order

class OrderExporter:
    """
    Класс для экспорта заявок в различные форматы.
    Поддерживает Excel (XLSX) и PDF.
    """
    
    @staticmethod
    def export_to_excel(queryset):
        """
        Экспорт заявок в Excel.
        Возвращает HttpResponse с файлом.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Заявки"
        
        # Заголовки
        headers = [
            "ID", "Клиент", "Телефон", "Адрес", 
            "Статус", "Дата создания", "Менеджер"
        ]
        ws.append(headers)
        
        # Данные
        for order in queryset:
            ws.append([
                order.id,
                order.client_name,
                order.phone,
                str(order.address),
                order.get_status_display(),
                order.created_at.strftime("%d.%m.%Y %H:%M"),
                str(order.assigned_to) if order.assigned_to else ""
            ])
        
        # Настройка стилей
        for column in ws.columns:
            max_length = 0
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column[0].column_letter].width = adjusted_width
        
        # Сохранение в HttpResponse
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=orders_{datetime.now().strftime("%Y%m%d")}.xlsx'
        wb.save(response)
        
        return response

    @staticmethod
    def export_to_pdf(queryset):
        """
        Экспорт заявок в PDF.
        Возвращает HttpResponse с файлом.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=orders_{datetime.now().strftime("%Y%m%d")}.pdf'
        
        p = canvas.Canvas(response)
        y = 800  # Начальная позиция по Y
        
        # Заголовок
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Отчет по заявкам")
        y -= 30
        
        # Данные
        p.setFont("Helvetica", 10)
        for order in queryset:
            p.drawString(50, y, f"ID: {order.id}")
            p.drawString(150, y, f"Клиент: {order.client_name}")
            p.drawString(350, y, f"Статус: {order.get_status_display()}")
            y -= 20
            
            p.drawString(50, y, f"Адрес: {order.address}")
            p.drawString(350, y, f"Дата: {order.created_at.strftime('%d.%m.%Y')}")
            y -= 20
            
            p.drawString(50, y, f"Менеджер: {order.assigned_to if order.assigned_to else 'Не назначен'}")
            y -= 30
            
            if y < 50:  # Проверка на конец страницы
                p.showPage()
                y = 800
                p.setFont("Helvetica", 10)
        
        p.save()
        return response