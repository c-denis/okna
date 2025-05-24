import httpClient from '@/utils/httpClient';
import type { AxiosResponse } from 'axios';

/**
 * Статусы заявок в системе.
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
 */
export interface RequestCreateData {
  client_name: string;
  phone: string;
  address: string;
  comment?: string;
  city_id?: number;
}

/**
 * Модель менеджера.
 */
interface Manager {
  id: number;
  name: string;
  status: 'free' | 'busy' | 'dayoff' | 'training';
}

/**
 * Элемент истории изменения статуса.
 */
interface StatusHistoryItem {
  status: RequestStatus;
  changed_at: string;
  changed_by: string;
  comment?: string;
}

/**
 * Полная модель заявки с сервера.
 */
export interface ApiRequest extends RequestCreateData {
  id: number;
  status: RequestStatus;
  created_at: string;
  updated_at?: string;
  assigned_to?: Manager;
  is_blacklisted: boolean;
  status_history?: StatusHistoryItem[];
}

/**
 * Данные для назначения заявки.
 */
export interface AssignRequestPayload {
  manager_id: number;
  force?: boolean;
}

/**
 * Параметры фильтрации заявок.
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
 * Данные для обновления статуса заявки.
 */
export interface UpdateStatusData {
  status: RequestStatus;
  comment?: string;
}

/**
 * Назначает заявку на менеджера.
 */
export const assignRequest = async (
  requestId: number,
  data: AssignRequestPayload | number
): Promise<ApiRequest> => {
  try {
    const payload: AssignRequestPayload = typeof data === 'number'
      ? { manager_id: data }
      : data;

    const response: AxiosResponse<ApiRequest> = await httpClient.patch(
      `/api/v1/orders/${requestId}/assign/`,
      payload
    );

    return response.data;
  } catch (error) {
    console.error(`Error assigning request ${requestId}:`, error);
    throw handleBackendError(error);
  }
};

// Остальные функции API остаются без изменений
// (fetchRequests, createRequest, updateRequestStatus и т.д.)

function handleBackendError(error: any): Error {
  if (error.response?.data) {
    if (typeof error.response.data.detail === 'string') {
      return new Error(error.response.data.detail);
    }
    if (typeof error.response.data === 'object') {
      const firstError = Object.values<string[]>(error.response.data)[0]?.[0];
      if (firstError) {
        return new Error(firstError);
      }
    }
  }
  return new Error('Ошибка соединения с сервером');
}
