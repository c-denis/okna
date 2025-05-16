<template>
  <div class="main-layout">
    <aside class="sidebar">
      <nav class="nav">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          active-class="active"
        >
          <component :is="link.icon" class="icon" />
          <span class="text">{{ link.text }}</span>
        </router-link>
      </nav>
      <div class="user-panel">
        <div class="user-info">
          <span class="name">{{ user.name }}</span>
          <span class="role">{{ roleName }}</span>
        </div>
        <button class="logout-btn" @click="logout">
          <LogoutIcon />
        </button>
      </div>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useRouter } from 'vue-router'
import {
  RequestsIcon,
  DashboardIcon,
  UsersIcon,
  ReportsIcon,
  LogoutIcon
} from '@/components/icons'

const authStore = useAuthStore()
const router = useRouter()

const user = computed(() => authStore.user || { name: '', role: '' })

const roleName = computed(() => {
  const roles: Record<string, string> = {
    admin: 'Администратор',
    coordinator: 'Координатор',
    manager: 'Менеджер',
    operator: 'Оператор'
  }
  return roles[user.value.role] || user.value.role
})

const navLinks = computed(() => {
  const baseLinks = [
    { to: '/', text: 'Дашборд', icon: DashboardIcon },
    { to: '/requests', text: 'Заявки', icon: RequestsIcon }
  ]

  if (['admin', 'coordinator'].includes(user.value.role)) {
    baseLinks.push(
      { to: '/reports', text: 'Отчёты', icon: ReportsIcon }
    )
  }

  if (user.value.role === 'admin') {
    baseLinks.push(
      { to: '/users', text: 'Пользователи', icon: UsersIcon }
    )
  }

  return baseLinks
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: #2c3e50;
  color: white;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
}

.nav {
  flex-grow: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #ecf0f1;
  text-decoration: none;
  transition: background 0.3s;
}

.nav-link:hover {
  background: #34495e;
}

.nav-link.active {
  background: #3498db;
}

.icon {
  margin-right: 12px;
  width: 20px;
  height: 20px;
}

.content {
  padding: 20px;
  background: #f5f7fa;
}

.user-panel {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #34495e;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.name {
  font-weight: 500;
}

.role {
  font-size: 0.8rem;
  opacity: 0.8;
}

.logout-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
