import { defineStore } from 'pinia'
import axios from '@utils/httpClient'
import router from '@/router'
import type { User } from '@/types/users.d'

interface AuthState {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    async login(email: string, password: string) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/auth/login', { email, password })
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('authToken', this.token)
        router.push('/')
      } catch (error) {
        this.error = 'Неверный email или пароль'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('authToken')
      router.push('/login')
    },

    async checkAuth() {
      const token = localStorage.getItem('authToken')
      if (token) {
        try {
          this.token = token
          const response = await axios.get('/auth/me')
          this.user = response.data
        } catch (error) {
          this.logout()
        }
      }
    }
  }
})
