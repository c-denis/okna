import httpClient from '@/utils/httpClient';
import type { AxiosResponse } from 'axios';

/**
 * Статусы заявок в системе.
 * Соответствуют статусам на backend (Django модель Order)
 */
export enum RequestStatus {
  UNASSIGNED = 'unassigned',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REJECTED = 'rejected'
}

/**
 * Данные для создания новой заявки.
 * Соответствует сериализатору OrderCreateSerializer в Django
 */
export interface RequestCreateData {
  client_name: string;
  phone: string;
  address: string;
  comment?: string;
  city_id?: number;  // Для связи с моделью City
}

/**
 * Полная модель заявки с сервера.
 * Соответствует сериализатору OrderSerializer в Django
 */
export interface Request extends RequestCreateData {
  id: number;
  status: RequestStatus;
  created_at: string;
  updated_at?: string;
  assigned_to?: Manager;
  is_blacklisted: boolean;
  status_history?: StatusHistoryItem[];
}

/**
 * Модель менеджера для назначения заявок.
 * Соответствует UserSerializer в Django
 */
interface Manager {
  id: number;
  name: string;
  status: 'free' | 'busy' | 'dayoff' | 'training';
}

/**
 * Элемент истории изменения статуса.
 * Соответствует StatusHistorySerializer в Django
 */
interface StatusHistoryItem {
  status: RequestStatus;
  changed_at: string;
  changed_by: string;
}

/**
 * Параметры фильтрации заявок.
 * Соответствует параметрам в OrderViewSet (Django REST)
 */
export interface RequestFilterParams {
  status?: RequestStatus;
  manager_id?: number;
  city_id?: number;
  date_from?: string;
  date_to?: string;
  is_blacklisted?: boolean;
}

/**
 * Получает список заявок с возможностью фильтрации
 * @param params Параметры фильтрации
 * @returns Promise с массивом заявок
 */
export const fetchRequests = async (params?: RequestFilterParams): Promise<Request[]> => {
  try {
    const response: AxiosResponse<Request[]> = await httpClient.get('/api/v1/orders/', {
      params,
      paramsSerializer: { indexes: null }  // Для правильной сериализации массивов
    });

    // Трансформация данных при необходимости
    return response.data.map(request => ({
      ...request,
      created_at: formatServerDate(request.created_at),
      updated_at: request.updated_at ? formatServerDate(request.updated_at) : undefined
    }));
  } catch (error) {
    console.error('Error fetching requests:', error);
    throw new Error('Не удалось загрузить заявки. Пожалуйста, попробуйте позже.');
  }
};

/**
 * Создает новую заявку
 * @param data Данные для создания заявки
 * @returns Promise с созданной заявкой
 */
export const createRequest = async (data: RequestCreateData): Promise<Request> => {
  try {
    // Валидация телефона перед отправкой
    if (!isValidPhone(data.phone)) {
      throw new Error('Неверный формат телефона');
    }

    const response: AxiosResponse<Request> = await httpClient.post('/api/v1/orders/', data);
    return {
      ...response.data,
      created_at: formatServerDate(response.data.created_at)
    };
  } catch (error) {
    console.error('Error creating request:', error);
    throw handleBackendError(error);
  }
};

/**
 * Назначает заявку на менеджера
 * @param requestId ID заявки
 * @param managerId ID менеджера
 * @returns Promise с обновленной заявкой
 */
export const assignRequest = async (requestId: number, managerId: number): Promise<Request> => {
  try {
    const response: AxiosResponse<Request> = await httpClient.patch(
      `/api/v1/orders/${requestId}/assign/`,
      { manager_id: managerId }
    );
    return response.data;
  } catch (error) {
    console.error(`Error assigning request ${requestId}:`, error);
    throw handleBackendError(error);
  }
};

/**
 * Обновляет статус заявки
 * @param requestId ID заявки
 * @param status Новый статус
 * @param comment Комментарий к изменению (опционально)
 * @returns Promise с обновленной заявкой
 */
export const updateRequestStatus = async (
  requestId: number,
  status: RequestStatus,
  comment?: string
): Promise<Request> => {
  try {
    const payload = { status };
    if (comment) payload.comment = comment;

    const response: AxiosResponse<Request> = await httpClient.patch(
      `/api/v1/orders/${requestId}/status/`,
      payload
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating status for request ${requestId}:`, error);
    throw handleBackendError(error);
  }
};

/**
 * Получает детальную информацию о заявке
 * @param requestId ID заявки
 * @returns Promise с деталями заявки
 */
export const getRequestDetails = async (requestId: number): Promise<Request> => {
  try {
    const response: AxiosResponse<Request> = await httpClient.get(`/api/v1/orders/${requestId}/`);
    return {
      ...response.data,
      created_at: formatServerDate(response.data.created_at),
      updated_at: response.data.updated_at ? formatServerDate(response.data.updated_at) : undefined,
      status_history: response.data.status_history?.map(item => ({
        ...item,
        changed_at: formatServerDate(item.changed_at)
      }))
    };
  } catch (error) {
    console.error(`Error fetching details for request ${requestId}:`, error);
    throw handleBackendError(error);
  }
};

/**
 * Добавляет клиента в черный список
 * @param requestId ID заявки
 * @param reason Причина добавления
 * @returns Promise с обновленной заявкой
 */
export const addToBlacklist = async (requestId: number, reason: string): Promise<Request> => {
  try {
    const response: AxiosResponse<Request> = await httpClient.post(
      `/api/v1/orders/${requestId}/blacklist/`,
      { reason }
    );
    return response.data;
  } catch (error) {
    console.error(`Error adding to blacklist request ${requestId}:`, error);
    throw handleBackendError(error);
  }
};

/** Вспомогательные функции */

/**
 * Форматирует дату с сервера в локальный формат
 */
function formatServerDate(dateString: string): string {
  return new Date(dateString).toLocaleString('ru-RU');
}

/**
 * Проверяет валидность номера телефона
 */
function isValidPhone(phone: string): boolean {
  return /^\+?[0-9\s\-\(\)]{10,20}$/.test(phone);
}

/**
 * Обрабатывает ошибки от backend
 */
function handleBackendError(error: any): Error {
  if (error.response) {
    // Стандартные ошибки Django REST
    const detail = error.response.data.detail ||
      Object.values(error.response.data)[0]?.[0] ||
      'Ошибка сервера';
    return new Error(typeof detail === 'string' ? detail : 'Неверные данные');
  }
  return new Error('Ошибка соединения с сервером');
}
