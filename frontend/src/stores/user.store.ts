import { defineStore } from 'pinia'
import axios from '@/utils/httpClient'
import { UserRole, ManagerStatus } from '@/types/users' // Изменено с import type на обычный import
import type { User, Manager, Leader } from '@/types/users'
import type { UserCreateData } from '@/types/users'

/**
 * Интерфейс состояния хранилища пользователей
 */
interface UsersState {
  users: User[]
  managers: Manager[]
  leaders: Leader[]
  loading: boolean
  error: string | null
  currentUser: User | null
}

/**
 * Хранилище для работы с пользователями системы
 */
export const useUsersStore = defineStore('users', {
  state: (): UsersState => ({
    users: [],
    managers: [],
    leaders: [],
    loading: false,
    error: null,
    currentUser: null
  }),

  getters: {
    getManagersByCity: (state) => (cityId: number) => {
      return state.managers.filter(m => m.city_id === cityId)
    },

    availableManagers: (state) => {
      return state.managers.filter(m =>
        m.status === ManagerStatus.AVAILABLE && // Теперь ManagerStatus доступен как значение
        m.current_assignments < m.max_assignments
      )
    },

    getManagerById: (state) => (id: string) => {
      return state.managers.find(m => m.id === id)
    },

    canAssignRequests(): boolean {
      return this.currentUser?.role === UserRole.COORDINATOR || // Теперь UserRole доступен как значение
             this.currentUser?.role === UserRole.ADMIN
    }
  },

  actions: {
    /**
     * Создает нового пользователя
     */
    async createUser(userData: UserCreateData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/users', userData)
        this.users.push(response.data)
        return response.data
      } catch (error) {
        this.handleError(error, 'Ошибка создания пользователя')
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Загружает пользователя по ID
     */
    async fetchUserById(id: string) {
      this.loading = true
      try {
        const response = await axios.get(`/users/${id}`)
        return response.data
      } catch (error) {
        this.handleError(error, 'Ошибка загрузки пользователя')
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Обновляет данные пользователя
     */
    async updateUser(id: string, userData: Partial<User>) {
      this.loading = true
      try {
        const response = await axios.patch(`/users/${id}`, userData)
        const index = this.users.findIndex(u => u.id === id)
        if (index !== -1) {
          this.users[index] = { ...this.users[index], ...response.data }
        }
        return response.data
      } catch (error) {
        this.handleError(error, 'Ошибка обновления пользователя')
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Загружает список менеджеров
     */
    async fetchManagers(params?: { city_id?: number }) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/users/managers', { params })
        this.managers = response.data
        return response.data
      } catch (error) {
        this.handleError(error, 'Ошибка загрузки менеджеров')
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Обновляет статус менеджера
     */
    async updateManagerStatus(
      managerId: string,
      status: ManagerStatus, // ManagerStatus используется как значение
      requestId?: string
    ) {
      try {
        await axios.patch(`/users/managers/${managerId}/status`, {
          status,
          request_id: requestId
        })

        const manager = this.managers.find(m => m.id === managerId)
        if (manager) {
          manager.status = status
          manager.current_request_id = requestId || null
          manager.current_assignments =
            status === ManagerStatus.BUSY
              ? manager.current_assignments + 1
              : Math.max(0, manager.current_assignments - 1)
        }
      } catch (error) {
        this.handleError(error, 'Ошибка обновления статуса менеджера')
        throw error
      }
    },

    /**
     * Загружает данные текущего пользователя
     */
    async fetchCurrentUser() {
      this.loading = true
      try {
        const response = await axios.get('/users/me')
        this.currentUser = response.data
        return response.data
      } catch (error) {
        this.handleError(error, 'Ошибка загрузки данных пользователя')
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Метод обработки ошибок (убрано ключевое слово private)
     */
    handleError(error: unknown, defaultMessage: string) {
      const errorMessage = error instanceof Error
        ? error.message
        : defaultMessage

      this.error = errorMessage
      console.error('UsersStore error:', error)
      throw new Error(errorMessage)
    }
  }
})
