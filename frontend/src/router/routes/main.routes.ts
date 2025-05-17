import { RouteRecordRaw } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const mainRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: {
      layout: MainLayout,
      requiresAuth: true,
      title: 'Главная',
      roles: ['admin', 'manager', 'operator']
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: {
      layout: MainLayout,
      requiresAuth: true,
      title: 'Профиль'
    }
  },
  {
    path: '/requests',
    name: 'requests',
    component: () => import('@/views/ListView.vue'),
    meta: {
      layout: MainLayout,
      requiresAuth: true,
      title: 'Заявки',
      roles: ['admin', 'manager']
    }
  }
]

export default mainRoutes
