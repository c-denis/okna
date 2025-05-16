import { RouteRecordRaw } from 'vue-router'
import AuthLayout from '@/layouts/AuthLayout.vue'

const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Auth/LoginView.vue'),
    meta: {
      layout: AuthLayout,
      requiresAuth: false,
      title: 'Вход в систему'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/Auth/RegisterView.vue'),
    meta: {
      layout: AuthLayout,
      requiresAuth: false,
      title: 'Регистрация'
    }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('@/views/Auth/ForgotPasswordView.vue'),
    meta: {
      layout: AuthLayout,
      requiresAuth: false,
      title: 'Восстановление пароля'
    }
  }
]

export default authRoutes
