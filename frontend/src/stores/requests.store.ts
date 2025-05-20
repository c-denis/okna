import { defineStore } from 'pinia';
import {
  fetchRequests as fetchRequestsApi,
  createRequest as createRequestApi,
  assignRequest as assignRequestApi,
  updateRequestStatus as updateRequestStatusApi,
  getRequestDetails as getRequestDetailsApi,
  addToBlacklist as addToBlacklistApi,
  type Request,
  type RequestCreateData,
  type RequestStatus,
  type RequestFilterParams
} from '@/api/requests.api';
import { useAuthStore } from './auth.store';

export const useRequestsStore = defineStore('requests', {
  state: () => ({
    requests: [] as Request[],
    currentRequest: null as Request | null,
    loading: false,
    error: null as string | null,
    filters: {
      status: undefined as RequestStatus | undefined,
      city: undefined as string | undefined,
      search: undefined as string | undefined,
      date_from: undefined as string | undefined,
      date_to: undefined as string | undefined
    }
  }),

  actions: {
    async fetchRequests(params?: RequestFilterParams) {
      this.loading = true;
      this.error = null;
      try {
        const effectiveParams = { ...this.filters, ...params };
        this.requests = await fetchRequestsApi(effectiveParams);
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка загрузки заявок';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createRequest(requestData: RequestCreateData) {
      this.loading = true;
      try {
        const newRequest = await createRequestApi(requestData);
        this.requests.unshift(newRequest);
        return newRequest;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка создания заявки';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async assignRequest(requestId: number, managerId: number) {
      try {
        const updatedRequest = await assignRequestApi(requestId, managerId);
        this.updateRequestInStore(updatedRequest);
        return updatedRequest;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка назначения заявки';
        throw error;
      }
    },

    async updateRequestStatus(requestId: number, status: RequestStatus, comment?: string) {
      try {
        const updatedRequest = await updateRequestStatusApi(requestId, status, comment);
        this.updateRequestInStore(updatedRequest);
        return updatedRequest;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка обновления статуса';
        throw error;
      }
    },

    async fetchRequestDetails(requestId: number) {
      this.loading = true;
      try {
        this.currentRequest = await getRequestDetailsApi(requestId);
        return this.currentRequest;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка загрузки деталей';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async addToBlacklist(requestId: number, reason: string) {
      try {
        const updatedRequest = await addToBlacklistApi(requestId, reason);
        this.updateRequestInStore(updatedRequest);
        return updatedRequest;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Ошибка добавления в ЧС';
        throw error;
      }
    },

    updateRequestInStore(updatedRequest: Request) {
      const index = this.requests.findIndex(r => r.id === updatedRequest.id);
      if (index !== -1) {
        this.requests.splice(index, 1, updatedRequest);
      }
      if (this.currentRequest?.id === updatedRequest.id) {
        this.currentRequest = updatedRequest;
      }
    },

    resetCurrentRequest() {
      this.currentRequest = null;
    },

    setFilter<K extends keyof typeof this.filters>(key: K, value: typeof this.filters[K]) {
      this.filters[key] = value;
    },

    resetFilters() {
      this.filters = {
        status: undefined,
        city: undefined,
        search: undefined,
        date_from: undefined,
        date_to: undefined
      };
    }
  },

  getters: {
    filteredRequests(state) {
      return state.requests.filter(request => {
        const matchesSearch = !state.filters.search ||
          request.client_name.toLowerCase().includes(state.filters.search.toLowerCase()) ||
          request.address.toLowerCase().includes(state.filters.search.toLowerCase());

        const matchesStatus = !state.filters.status ||
          request.status === state.filters.status;

        const matchesCity = !state.filters.city ||
          request.city === state.filters.city;

        return matchesSearch && matchesStatus && matchesCity;
      });
    },

    unassignedRequests(state) {
      return state.requests.filter(r => r.status === 'unassigned');
    },

    assignedRequests(state) {
      return state.requests.filter(r => r.status === 'assigned');
    },

    inProgressRequests(state) {
      return state.requests.filter(r => r.status === 'in_progress');
    },

    getRequestById(state) {
      return (id: number) => state.requests.find(r => r.id === id);
    },

    userCanEdit(state) {
      const authStore = useAuthStore();
      return authStore.user?.role === 'coordinator' || authStore.user?.role === 'admin';
    }
  }
});
