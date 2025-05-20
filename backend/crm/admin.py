from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Order,
    User,
    Location,
    Blacklist,
    ManagerStatus,
    NotificationLog
)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'client_name', 
        'phone', 
        'get_address',
        'status', 
        'assigned_to',
        'created_at',
        'is_blacklisted'
    )
    list_filter = ('status', 'created_at', 'assigned_to')
    search_fields = ('client_name', 'phone', 'address')
    readonly_fields = ('created_at',)
    list_editable = ('status',)
    actions = ['mark_as_completed']

    def get_address(self, obj):
        return f"{obj.address.city}, {obj.address.street}"
    get_address.short_description = 'Адрес'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Отметить как выполненные"

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name',
        'role',
        'get_status'
    )
    list_filter = ('role', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'telegram_chat_id')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_status(self, obj):
        return obj.managerstatus.status if hasattr(obj, 'managerstatus') else '-'
    get_status.short_description = 'Статус менеджера'

class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'house', 'apartment')
    search_fields = ('city', 'street')
    list_filter = ('city',)

class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'reason', 'created_at')
    search_fields = ('client_name', 'phone')
    readonly_fields = ('created_at',)

class ManagerStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'last_updated')
    list_editable = ('status',)
    readonly_fields = ('last_updated',)

class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'recipient', 'message_type', 'created_at')
    readonly_fields = ('created_at',)
    list_filter = ('message_type', 'created_at')

# Регистрация моделей
admin.site.register(Order, OrderAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Blacklist, BlacklistAdmin)
admin.site.register(ManagerStatus, ManagerStatusAdmin)
admin.site.register(NotificationLog, NotificationLogAdmin)