import { createRouter, createWebHistory } from 'vue-router'
import { authRoutes } from './routes/auth.routes'
import { mainRoutes } from './routes/main.routes'
import { adminRoutes } from './routes/admin.routes'
import { setupAuthGuard } from './guards/auth.guard'
import { setupRoleGuard } from './guards/role.guard'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...authRoutes, ...mainRoutes, ...adminRoutes],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// Установка глобальных guards
setupAuthGuard(router)
setupRoleGuard(router)

export default router
