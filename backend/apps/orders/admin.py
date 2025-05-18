from django.contrib import admin
from .models import Order, Location
from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'colored_status', 'client_name', 'phone', 'location', 'manager', 'created_at')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('client_name', 'phone', 'address')
    raw_id_fields = ('manager',)
    date_hierarchy = 'created_at'
    
    def colored_status(self, obj):
        colors = {
            'unassigned': 'red',
            'assigned': 'orange',
            'in_progress': 'blue',
            'completed': 'green',
            'rejected': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Статус'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)