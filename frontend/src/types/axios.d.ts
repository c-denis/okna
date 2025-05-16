import 'axios'

declare module 'axios' {
  export interface AxiosRequestConfig {
    silent?: boolean // Дополнительные кастомные параметры
    retry?: number
  }
}
