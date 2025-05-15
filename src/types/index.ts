export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface User {
  id: number
  name: string
  email: string
}
