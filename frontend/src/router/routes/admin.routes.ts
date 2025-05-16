import { RouteRecordRaw } from 'vue-router'

export const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('@/views/Admin/DashboardView.vue'),
    meta: {
      layout: 'MainLayout',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/admin/users',
    name: 'user-management',
    component: () => import('@/views/Admin/UserManagementView.vue'),
    meta: {
      layout: 'MainLayout',
      requiresAuth: true,
      roles: ['admin']
    },
    children: [
      {
        path: 'create',
        name: 'user-create',
        component: () => import('@/views/Admin/UserCreateView.vue')
      },
      {
        path: ':id/edit',
        name: 'user-edit',
        component: () => import('@/views/Admin/UserEditView.vue'),
        props: true
      }
    ]
  },
  {
    path: '/admin/settings',
    name: 'system-settings',
    component: () => import('@/views/Admin/SettingsView.vue'),
    meta: {
      layout: 'MainLayout',
      requiresAuth: true,
      roles: ['admin']
    }
  }
]
