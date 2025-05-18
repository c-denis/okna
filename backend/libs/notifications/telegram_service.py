import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_telegram_notification(request_id, client_name, address, manager_chat_id=None):
    try:
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

        keyboard = [
            [InlineKeyboardButton("✅ Принять заявку", callback_data=f"accept_{request_id}"),
             InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{request_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"<b>🆕 Новая заявка #{request_id}</b>\n"
            f"👤 <b>Клиент:</b> {client_name}\n"
            f"📍 <b>Адрес:</b> {address}\n"
            f"\n<i>Выберите действие:</i>"
        )

        chat_id = manager_chat_id if manager_chat_id else settings.TELEGRAM_CHAT_ID
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    except telegram.error.TelegramError as e:
        logger.error(f"Telegram API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)