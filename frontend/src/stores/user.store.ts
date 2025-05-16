import { defineStore } from 'pinia'
import axios from '@/utils/httpClient'
import type { User, Manager } from '@/types/users'

interface UsersState {
  users: User[]
  managers: Manager[]
  loading: boolean
  error: string | null
}

export const useUsersStore = defineStore('users', {
  state: (): UsersState => ({
    users: [],
    managers: [],
    loading: false,
    error: null
  }),

  getters: {
    getManagerById: (state) => (id: string) => {
      return state.managers.find(manager => manager.id === id)
    },
    availableManagers: (state) => {
      return state.managers.filter(manager => manager.status === 'available')
    },
    busyManagers: (state) => {
      return state.managers.filter(manager => manager.status === 'busy')
    }
  },

  actions: {
    async fetchAllUsers() {
      this.loading = true
      try {
        const response = await axios.get('/users')
        this.users = response.data
      } catch (error) {
        this.error = 'Ошибка загрузки пользователей'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchManagers() {
      this.loading = true
      try {
        const response = await axios.get('/users/managers')
        this.managers = response.data
      } catch (error) {
        this.error = 'Ошибка загрузки менеджеров'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateManagerStatus(managerId: string, status: string) {
      try {
        await axios.patch(`/users/managers/${managerId}/status`, { status })
        const manager = this.managers.find(m => m.id === managerId)
        if (manager) {
          manager.status = status
        }
      } catch (error) {
        this.error = 'Ошибка обновления статуса'
        throw error
      }
    }
  }
})
