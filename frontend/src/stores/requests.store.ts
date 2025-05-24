import { defineStore } from 'pinia';
import httpClient from '@/utils/httpClient';
import { useAuthStore } from './auth.store';
import { useUsersStore } from './user.store';
import type {
  Request,
  RequestCreateData,
  RequestFilterParams,
  AssignRequestData,
  UpdateStatusData,
  StatusHistoryItem
} from '@/types/requests';
import { RequestStatus } from '@/types/requests';
import { ManagerStatus } from '@/types/users'; // Импортируем из правильного файла

/**
 * Интерфейс для заявки API (бэкенд формат)
 */
interface ApiRequest {
  id: number;
  client_name: string;
  phone: string;
  address: string;
  city?: string;
  city_id?: number;
  street?: string;
  house?: string;
  building?: string;
  apartment?: string;
  comment?: string;
  status: RequestStatus;
  created_at: string;
  updated_at?: string;
  assigned_to?: {
    id: number;
    name: string;
    status: ManagerStatus;
  };
  is_blacklisted: boolean;
  status_history?: Array<{
    id?: number;
    status: RequestStatus;
    changed_at: string;
    changed_by: string;
    comment?: string;
  }>;
}

/**
 * Параметры фильтрации для API
 */
interface ApiRequestFilterParams {
  status?: RequestStatus;
  manager_id?: number;
  city_id?: number;
  date_from?: string;
  date_to?: string;
  is_blacklisted?: boolean;
  search?: string;
}

/**
 * Состояние хранилища заявок
 */
interface RequestsState {
  requests: Request[];
  currentRequest: Request | null;
  loading: boolean;
  error: string | null;
  filters: RequestFilterParams;
}

export const useRequestsStore = defineStore('requests', {
  state: (): RequestsState => ({
    requests: [],
    currentRequest: null,
    loading: false,
    error: null,
    filters: {
      status: undefined,
      city_id: undefined,
      search: undefined,
      date_from: undefined,
      date_to: undefined
    }
  }),

  actions: {
    /**
     * Загружает заявки с сервера
     */
    async fetchRequests(params?: RequestFilterParams): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const apiParams: ApiRequestFilterParams = {
          ...this.filters,
          ...params,
          manager_id: params?.manager_id ? Number(params.manager_id) : undefined
        };

        const response = await httpClient.get<ApiRequest[]>('/api/v1/orders/', {
          params: apiParams
        });
        this.requests = response.data.map(this.convertApiRequest);
      } catch (error) {
        this.handleError(error, 'Ошибка загрузки заявок');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Создает новую заявку
     */
    async createRequest(requestData: RequestCreateData): Promise<Request> {
      this.loading = true;
      try {
        const response = await httpClient.post<ApiRequest>('/api/v1/orders/', requestData);
        const convertedRequest = this.convertApiRequest(response.data);
        this.requests.unshift(convertedRequest);
        return convertedRequest;
      } catch (error) {
        this.handleError(error, 'Ошибка создания заявки');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Обновляет заявку
     */
    async updateRequest(requestId: string, requestData: Partial<RequestCreateData>): Promise<Request> {
      this.loading = true;
      try {
        const response = await httpClient.patch<ApiRequest>(
          `/api/v1/orders/${requestId}`,
          requestData
        );
        const convertedRequest = this.convertApiRequest(response.data);
        this.updateRequestInStore(convertedRequest);
        return convertedRequest;
      } catch (error) {
        this.handleError(error, 'Ошибка обновления заявки');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Назначает заявку на менеджера
     */
    async assignRequest(requestId: string, data: AssignRequestData): Promise<Request> {
      const usersStore = useUsersStore();
      try {
        const payload = {
          manager_id: Number(data.manager_id),
          force: data.force
        };

        const response = await httpClient.patch<ApiRequest>(
          `/api/v1/orders/${requestId}/assign/`,
          payload
        );
        const convertedRequest = this.convertApiRequest(response.data);
        this.updateRequestInStore(convertedRequest);

        await usersStore.updateManagerStatus(
          data.manager_id,
          ManagerStatus.BUSY,
          requestId
        );

        return convertedRequest;
      } catch (error) {
        this.handleError(error, 'Ошибка назначения заявки');
        throw error;
      }
    },

    /**
     * Обновляет статус заявки
     */
    async updateRequestStatus(
      requestId: string,
      status: RequestStatus,
      comment?: string
    ): Promise<Request> {
      const usersStore = useUsersStore();
      try {
        const statusData: UpdateStatusData = { status, comment };
        const response = await httpClient.patch<ApiRequest>(
          `/api/v1/orders/${requestId}/status/`,
          statusData
        );
        const convertedRequest = this.convertApiRequest(response.data);
        this.updateRequestInStore(convertedRequest);

        if (status === 'completed' || status === 'rejected') {
          const managerId = convertedRequest.assigned_to?.id;
          if (managerId) {
            await usersStore.updateManagerStatus(
              managerId,
              ManagerStatus.AVAILABLE
            );
          }
        }

        return convertedRequest;
      } catch (error) {
        this.handleError(error, 'Ошибка обновления статуса');
        throw error;
      }
    },

    /**
     * Добавляет в черный список
     */
    async addToBlacklist(requestId: string, reason: string): Promise<Request> {
      try {
        const response = await httpClient.post<ApiRequest>(
          `/api/v1/orders/${requestId}/blacklist/`,
          { reason }
        );
        const convertedRequest = this.convertApiRequest(response.data);
        this.updateRequestInStore(convertedRequest);
        return convertedRequest;
      } catch (error) {
        this.handleError(error, 'Ошибка добавления в ЧС');
        throw error;
      }
    },

    /**
     * Обновляет заявку в хранилище
     */
    updateRequestInStore(request: Request): void {
      const index = this.requests.findIndex(r => r.id === request.id);
      if (index !== -1) {
        this.requests.splice(index, 1, request);
      }
      if (this.currentRequest?.id === request.id) {
        this.currentRequest = request;
      }
    },

    /**
     * Устанавливает фильтры
     */
    setFilters(filters: Partial<RequestFilterParams>): void {
      this.filters = { ...this.filters, ...filters };
    },

    /**
     * Сбрасывает фильтры
     */
    resetFilters(): void {
      this.filters = {
        status: undefined,
        city_id: undefined,
        search: undefined,
        date_from: undefined,
        date_to: undefined
      };
    },

    /**
     * Преобразует заявку из API формата в клиентский
     */
    convertApiRequest(apiRequest: ApiRequest): Request {
      return {
        ...apiRequest,
        id: apiRequest.id.toString(),
        city_id: apiRequest.city_id || 0,
        street: apiRequest.street || '',
        house: apiRequest.house || '',
        building: apiRequest.building || '',
        apartment: apiRequest.apartment || '',
        assigned_to: apiRequest.assigned_to ? {
          ...apiRequest.assigned_to,
          id: apiRequest.assigned_to.id.toString(),
          status: apiRequest.assigned_to.status
        } : undefined,
        status_history: apiRequest.status_history?.map((item, index) => ({
          id: item.id?.toString() || index.toString(),
          status: item.status,
          changed_at: item.changed_at,
          changed_by: item.changed_by,
          comment: item.comment
        } as StatusHistoryItem))
      };
    },

    /**
     * Обрабатывает ошибки
     */
    handleError(error: unknown, defaultMessage: string): void {
      this.error = error instanceof Error
        ? error.message
        : defaultMessage;
      console.error('RequestsStore error:', error);
    }
  },

  getters: {
    /**
     * Отфильтрованные заявки
     */
    filteredRequests(state): Request[] {
      return state.requests.filter(request => {
        const searchFilter = !state.filters.search ||
          request.client_name.toLowerCase().includes(state.filters.search.toLowerCase()) ||
          request.phone.includes(state.filters.search);

        const statusFilter = !state.filters.status ||
          request.status === state.filters.status;

        const cityFilter = !state.filters.city_id ||
          request.city_id === state.filters.city_id;

        const dateFrom = state.filters.date_from
          ? new Date(state.filters.date_from)
          : null;
        const dateTo = state.filters.date_to
          ? new Date(state.filters.date_to)
          : null;

        const dateFilter = (!dateFrom || new Date(request.created_at) >= dateFrom) &&
          (!dateTo || new Date(request.created_at) <= dateTo);

        return searchFilter && statusFilter && cityFilter && dateFilter;
      });
    },

    /**
     * Не назначенные заявки
     */
    unassignedRequests(state): Request[] {
      return state.requests.filter(r => r.status === RequestStatus.UNASSIGNED);
    },

    /**
     * Заявки в работе
     */
    inProgressRequests(state): Request[] {
      return state.requests.filter(r => r.status === RequestStatus.IN_PROGRESS);
    },

    /**
     * Завершенные заявки
     */
    completedRequests(state): Request[] {
      return state.requests.filter(r => r.status === RequestStatus.COMPLETED);
    }
  }
});
