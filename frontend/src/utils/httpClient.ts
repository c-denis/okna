// frontend/src/utils/httpClient.ts
import axios, {
  type AxiosInstance,
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  type AxiosError
} from 'axios';

// Типы для API ответа
export interface ApiResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
}

// Конфигурация клиента
const createHttpClient = (): AxiosInstance => {
  const api: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    withCredentials: true
  });

  // Request interceptor
  api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error: AxiosError) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor
  api.interceptors.response.use(
    (response: AxiosResponse) => {
      // Можно преобразовать ответ здесь
      return {
        ...response,
        data: response.data
      };
    },
    (error: AxiosError) => {
      // Централизованная обработка ошибок
      if (error.response?.status === 401) {
        // Обработка неавторизованного доступа
        window.location.href = '/auth/login';
      }

      return Promise.reject({
        status: error.response?.status,
        message: error.message,
        data: error.response?.data
      });
    }
  );

  return api;
};

axios.interceptors.response.use(
  response => response,
  error => {
    // Обработка ошибок
    return Promise.reject(error);
  }
);

const httpClient = createHttpClient();

export default httpClient;
