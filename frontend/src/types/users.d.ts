/**
 * Типы и интерфейсы для работы с пользователями системы
 * Все идентификаторы приведены к строковому типу для совместимости с API
 */

/**
 * Роли пользователей в системе
 * @enum {string}
 */
export enum UserRole {
  /** Администратор системы */
  ADMIN = 'admin',
  /** Координатор (может назначать заявки) */
  COORDINATOR = 'coordinator',
  /** Менеджер/мастер (исполнитель заявок) */
  MANAGER = 'manager',
  /** Лидер/старший менеджер */
  LEADER = 'leader',
  /** Оператор (только создание заявок) */
  OPERATOR = 'operator'
}

/**
 * Статусы менеджера для отображения в интерфейсе
 * Соответствуют статусам на бэкенде
 * @enum {string}
 */
export enum ManagerStatus {
  /** Свободен, может принимать заявки */
  AVAILABLE = 'available',
  /** Занят выполнением заявки */
  BUSY = 'busy',
  /** Выходной день */
  DAY_OFF = 'dayoff',
  /** На обучении */
  TRAINING = 'training',
  /** Работает в паре с другим менеджером */
  PAIRED = 'paired'
}

/**
 * Тип для строкового представления статуса менеджера
 * Может использоваться в компонентах UI
 */
export type ManagerStatusType = keyof typeof ManagerStatus;

/**
 * Базовый интерфейс пользователя системы
 */
export interface BaseUser {
  /** Уникальный идентификатор пользователя */
  id: string;
  /** Полное имя пользователя */
  name: string;
  /** Электронная почта (используется для входа) */
  email: string;
  /** Контактный телефон */
  phone: string;
  /** Роль в системе */
  role: UserRole;
  /** Идентификатор города (опционально) */
  city_id?: number;
  /** URL аватара пользователя (опционально) */
  avatar?: string;
}

/**
 * Интерфейс менеджера (исполнителя заявок) с дополнительными полями
 */
export interface Manager extends BaseUser {
  /** Фиксированная роль - менеджер */
  role: UserRole.MANAGER;
  /** Текущий статус менеджера */
  status: ManagerStatus;
  /** ID чата в Telegram для уведомлений */
  telegram_chat_id: string;
  /** ID текущей заявки (null если нет активной заявки) */
  current_request_id: string | null;
  /** Максимальное количество одновременных назначений */
  max_assignments: number;
  /** Текущее количество назначений */
  current_assignments: number;
  /** Специализация (например, "Окна", "Двери") */
  specialization?: string;
  /** Время последней активности */
  last_activity?: string;
}

/**
 * Интерфейс лидера (старшего менеджера/координатора)
 */
export interface Leader extends BaseUser {
  /** Фиксированная роль - лидер */
  role: UserRole.LEADER;
  /** Массив ID городов под управлением */
  managed_cities: number[];
  /** Может ли подтверждать заявки */
  can_approve: boolean;
}

/**
 * Интерфейс администратора системы
 */
export interface Admin extends BaseUser {
  /** Фиксированная роль - администратор */
  role: UserRole.ADMIN;
  /** Список прав доступа */
  permissions: string[];
}

/**
 * Тип для всех пользователей системы (объединение интерфейсов)
 */
export type User = Manager | Leader | Admin | BaseUser;

/**
 * Тип для данных создания нового пользователя
 */
export interface UserCreateData {
  name: string;
  email: string;
  phone: string;
  role: UserRole;
  city_id?: number;
  password: string;
  /** Только для менеджеров */
  telegram_chat_id?: string;
  max_assignments?: number;
  specialization?: string;
}

/**
 * Тип для краткого отображения менеджера в выпадающих списках
 */
export interface ManagerShortInfo {
  /** ID менеджера */
  id: string;
  /** Имя менеджера */
  name: string;
  /** Текущий статус */
  status: ManagerStatus;
  /** Специализация (опционально) */
  specialization?: string;
}

/**
 * Тип для обновления данных пользователя
 */
export interface UserUpdateData {
  name?: string;
  email?: string;
  phone?: string;
  city_id?: number | null;
  avatar?: string | null;
  /** Только для менеджеров */
  telegram_chat_id?: string;
  max_assignments?: number;
  specialization?: string;
  /** Для изменения пароля */
  password?: string;
  current_password?: string;
}

/**
 * Тип для данных аутентификации
 */
export interface AuthData {
  email: string;
  password: string;
  remember?: boolean;
}

/**
 * Тип для ответа при успешной аутентификации
 */
export interface AuthResponse {
  user: User;
  token: string;
  expires_in: number;
}
