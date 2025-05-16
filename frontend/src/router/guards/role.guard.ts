import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

export const setupRoleGuard = (router: Router) => {
  router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Если нет ограничений по ролям
    if (!to.meta.roles) return next()

    // Проверка ролей
    if (!to.meta.roles.includes(authStore.userRole)) {
      return next({ name: 'forbidden' })
    }

    next()
  })
}
