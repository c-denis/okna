import { ManagerStatus } from './users'; // Импортируем enum статусов
export interface ReportData {
  total: number;
  completed: number;
  rejected: number;
  averageTime: string;
  byStatus: Array<{
    status: string;
    count: number;
  }>;
  byCity: Array<{
    city: string;
    total: number;
    completed: number;
  }>;
}

export interface ManagerStats {
  id: number;
  name: string;
  completed: number;
  rejected: number;
  efficiency: number;
  lastActivity?: string;
}

/**
 * Статусы заявки в системе
 * Соответствуют статусам в БД на бэкенде
 */
export enum RequestStatus {
  UNASSIGNED = 'unassigned',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REJECTED = 'rejected',
  CANCELLED = 'cancelled'
}

/**
 * Данные для создания новой заявки
 */
export interface RequestCreateData {
  client_name: string;
  phone: string;
  address: string;
  city?: string;
  city_id: number;
  street?: string;
  house?: string;
  building?: string;
  apartment?: string;
  comment?: string;
  priority?: 'low' | 'medium' | 'high';
  operator_id?: string;
}

/**
 * Элемент истории изменения статуса заявки
 */
export interface StatusHistoryItem {
  id: string; // Обязательное поле
  status: RequestStatus;
  changed_at: string;
  changed_by: string;
  changed_by_user?: {
    id: string;
    name: string;
    role: string;
  };
  comment?: string;
}

/**
 * Полная модель заявки для фронтенда
 */
export interface Request extends Omit<RequestCreateData, 'operator_id'> {
  id: string;
  status: RequestStatus;
  created_at: string;
  updated_at?: string;
  assigned_to?: {
    id: string;
    name: string;
    status: ManagerStatus; // Используем импортированный enum
  };
  is_blacklisted: boolean;
  status_history?: StatusHistoryItem[];
  operator?: {
    id: string;
    name: string;
  };
  street: string;
  house: string;
  building: string;
  apartment: string;
}

/**
 * Параметры фильтрации заявок
 */
export interface RequestFilterParams {
  status?: RequestStatus;
  manager_id?: string; // На клиенте это строка
  city_id?: number;
  date_from?: string;
  date_to?: string;
  is_blacklisted?: boolean;
  search?: string;
}

/**
 * Данные для назначения заявки
 */
export interface AssignRequestData {
  manager_id: string;
  force?: boolean;
}

/**
 * Данные для обновления статуса заявки
 */
export interface UpdateStatusData {
  status: RequestStatus;
  comment?: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
}
