from django.apps import AppConfig

class CRMConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'
    
    def ready(self):
        # Импорт сигналов и задач
        import crm.signals
        from .services import notification_service
        
        # Инициализация Telegram бота при запуске приложения
        notification_service.initialize_bot()