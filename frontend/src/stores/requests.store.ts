import { defineStore } from 'pinia';
import axios from '@/api/client';
import {
  fetchRequests as fetchRequestsApi,
  createRequest as createRequestApi,
  assignRequest as assignRequestApi,
  updateRequestStatus as updateRequestStatusApi,
  getRequestDetails as getRequestDetailsApi
} from '@/api/requests.api';
import type { Request, RequestData, RequestStatus } from '@/types/requests';

export const useRequestsStore = defineStore('requests', {
  state: () => ({
    requests: [] as Request[],
    loading: false,
    error: null as string | null,
    currentRequest: null as Request | null
  }),

  actions: {
    // Загрузка всех заявок
    async fetchRequests() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetchRequestsApi();
        this.requests = response.data;
      } catch (error) {
        this.error = 'Ошибка загрузки заявок';
        console.error(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Создание новой заявки
    async createRequest(requestData: RequestData) {
      this.loading = true;
      try {
        const response = await createRequestApi(requestData);
        this.requests.unshift(response.data);
        return response.data;
      } catch (error) {
        this.error = 'Ошибка создания заявки';
        console.error(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Назначение заявки менеджеру
    async assignRequest(requestId: string, managerId: string) {
      try {
        await assignRequestApi(requestId, managerId);
        const request = this.requests.find(r => r.id === requestId);
        if (request) {
          request.status = 'assigned';
          request.managerId = managerId;
        }
      } catch (error) {
        this.error = 'Ошибка назначения заявки';
        console.error(error);
        throw error;
      }
    },

    // Обновление статуса заявки
    async updateRequestStatus(requestId: string, status: RequestStatus) {
      try {
        await updateRequestStatusApi(requestId, status);
        const request = this.requests.find(r => r.id === requestId);
        if (request) {
          request.status = status;
          request.updatedAt = new Date().toISOString();
        }
      } catch (error) {
        this.error = 'Ошибка обновления статуса';
        console.error(error);
        throw error;
      }
    },

    // Добавление клиента в черный список
    async blacklistRequest(requestId: string) {
      try {
        await axios.patch(`/requests/${requestId}/blacklist`);
        const request = this.requests.find(r => r.id === requestId);
        if (request) {
          request.isBlacklisted = true;
        }
      } catch (error) {
        this.error = 'Ошибка добавления в черный список';
        console.error(error);
        throw error;
      }
    },

    // Загрузка деталей конкретной заявки
    async fetchRequestDetails(requestId: string) {
      this.loading = true;
      try {
        const response = await getRequestDetailsApi(requestId);
        this.currentRequest = response.data;
        return response.data;
      } catch (error) {
        this.error = 'Ошибка загрузки деталей заявки';
        console.error(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Сброс текущей заявки
    resetCurrentRequest() {
      this.currentRequest = null;
    }
  },

  getters: {
    // Получение заявок по статусу
    getRequestsByStatus: (state) => {
      return (status: RequestStatus) => state.requests.filter(r => r.status === status);
    },

    // Получение заявки по ID
    getRequestById: (state) => {
      return (id: string) => state.requests.find(r => r.id === id);
    },

    // Получение незавершенных заявок
    getActiveRequests: (state) => {
      return state.requests.filter(r =>
        ['unassigned', 'assigned', 'in_progress'].includes(r.status)
      );
    }
  }
});
