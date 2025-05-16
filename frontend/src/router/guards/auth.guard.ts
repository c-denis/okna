import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

export const setupAuthGuard = (router: Router) => {
  router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Для маршрутов, не требующих авторизации
    if (!to.meta.requiresAuth) return next()

    // Проверка аутентификации
    if (!authStore.isAuthenticated) {
      return next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    }

    next()
  })
}
