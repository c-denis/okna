import axios from '@/utils/httpClient';
import type { ReportData, ManagerStats } from '@/types/reports';

export default {
  /**
   * Получить сводную статистику
   * @param params Параметры фильтрации
   */
  async fetchReports(params?: {
    period?: 'day' | 'week' | 'month';
    dateFrom?: string;
    dateTo?: string;
  }): Promise<ReportData> {
    const response = await axios.get('/api/reports', { params });
    return response.data;
  },

  /**
   * Получить статистику менеджера
   * @param managerId ID менеджера
   */
  async fetchManagerStats(managerId: number): Promise<ManagerStats> {
    const response = await axios.get(`/api/managers/${managerId}/stats`);
    return response.data;
  }
};
