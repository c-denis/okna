declare module 'axios' {
  export interface AxiosRequestConfig {
    silent?: boolean // Дополнительное кастомное поле
  }
}

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}
