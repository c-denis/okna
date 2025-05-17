from django.contrib import admin
from .models import City, Client, Manager, Request


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'get_active_requests', 'get_rejected_today')
    list_filter = ('status',)

    def get_active_requests(self, obj):
        return obj.request_set.filter(status='assigned').count()

    get_active_requests.short_description = 'Активные заявки'

    def get_rejected_today(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return obj.request_set.filter(
            status='rejected',
            updated_at__date=today
        ).count()

    get_rejected_today.short_description = 'Отказов сегодня'


admin.site.register(City)
admin.site.register(Client)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Request)