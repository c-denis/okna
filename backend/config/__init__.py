# Инициализация пакета конфигурации
default_app_config = 'config.apps.ConfigConfig'

# Импорт настроек Celery при старте проекта
from .celery import app as celery_app

__all__ = ('celery_app',)