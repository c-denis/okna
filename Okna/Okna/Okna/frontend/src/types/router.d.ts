// router/types.d.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    layout?: 'MainLayout' | 'AuthLayout'
    requiresAuth?: boolean
    roles?: ('admin' | 'coordinator' | 'manager' | 'operator')[]
  }
}
