import axios from '@/utils/httpClient';
import type { Manager } from '@/types/users'; // Добавляем импорт типа Manager
import type { Request } from '@/types/requests'; // Добавляем импорт типа Request

/**
 * Композиция для работы с Telegram API
 */
export const useTelegram = () => {
  /**
   * Отправка уведомления менеджеру
   * @param chatId - ID чата в Telegram
   * @param message - Текст сообщения
   */
  const sendNotification = async (chatId: string, message: string) => {
    try {
      await axios.post('/api/telegram/notify', {
        chat_id: chatId,
        text: message
      });
    } catch (error) {
      console.error('Ошибка отправки Telegram уведомления:', error);
      throw new Error('Не удалось отправить уведомление');
    }
  };

  /**
   * Отправка уведомления о новой заявке
   * @param manager - Объект менеджера
   * @param request - Данные заявки
   */
  const sendRequestNotification = async (manager: Manager, request: Request) => {
    const message = `Новая заявка №${request.id}\nКлиент: ${request.client_name}\nАдрес: ${request.address}`;
    return sendNotification(manager.telegram_chat_id, message);
  };

  return {
    sendNotification,
    sendRequestNotification
  };
};
