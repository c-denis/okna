from django.apps import AppConfig
from django.conf import settings  # Добавьте этот импорт
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

    def ready(self):
        """Инициализация при запуске приложения"""
        self._ensure_logs_dir_exists()

        # Добавьте эту проверку для избежания двойной инициализации
        if os.environ.get('RUN_MAIN') == 'true':
            if not settings.DEBUG:  # Теперь settings доступен
                self._setup_telegram_bot()

    def _ensure_logs_dir_exists(self):
        """Создает папку для логов если ее нет"""
        logs_dir = Path(__file__).parent.parent / 'logs'
        try:
            logs_dir.mkdir(exist_ok=True, mode=0o777)
        except Exception as e:
            logger.error(f"Не удалось создать папку для логов: {str(e)}")

    def _setup_telegram_bot(self):
        """Настройка Telegram бота"""
        try:
            from telegram import Bot
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            bot.delete_webhook()
            bot.set_webhook(
                url=settings.TELEGRAM_WEBHOOK_URL,
                allowed_updates=['message', 'callback_query']
            )
            logger.info("Telegram webhook успешно настроен")
        except Exception as e:
            logger.error(f"Ошибка настройки Telegram: {str(e)}", exc_info=True)