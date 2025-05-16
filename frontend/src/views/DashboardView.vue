<template>
  <div class="dashboard-view">
    <!-- Заголовок и быстрые действия -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">
        <DashboardIcon size="24" class="title-icon" />
        Рабочий стол
      </h1>
      <div class="quick-actions">
        <button class="action-btn" @click="navigateToRequests">
          <RequestsIcon :size="20" />
          <span>Создать заявку</span>
        </button>
      </div>
    </div>

    <!-- Карточки статистики -->
    <div class="stats-grid">
      <StatsCard
        title="Новые заявки"
        :value="stats.newRequests"
        trend="+12%"
        icon="requests"
        color="blue"
      >
        <template #icon>
          <RequestsIcon class="stats-icon" />
        </template>
      </StatsCard>

      <StatsCard
        title="В работе"
        :value="stats.inProgress"
        trend="+3"
        icon="in-progress"
        color="orange"
      >
        <template #icon>
          <StatusBadge status="in_progress" />
        </template>
      </StatsCard>

      <StatsCard
        title="Мои задачи"
        :value="stats.myTasks"
        trend="-2"
        icon="user"
        color="green"
      >
        <template #icon>
          <UsersIcon class="text-green-500" />
        </template>
      </StatsCard>
    </div>

    <!-- Последние заявки -->
    <div class="recent-section">
      <h2 class="section-title">
        <HistoryIcon :size="20" class="mr-2" />
        Последние заявки
      </h2>
      <RequestsTable :requests="recentRequests" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRequestsStore } from '@/stores/requests.store'
import {
  DashboardIcon,
  RequestsIcon,
  UsersIcon,
  HistoryIcon
} from '@/components/icons'
import StatsCard from '@/components/ui/StatsCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import RequestsTable from '@/components/features/Requests/RequestsTable.vue'

const router = useRouter()
const requestsStore = useRequestsStore()

const stats = ref({
  newRequests: 15,
  inProgress: 8,
  myTasks: 5
})

const recentRequests = ref<any[]>([])

const navigateToRequests = () => {
  router.push('/requests/new')
}

onMounted(async () => {
  await requestsStore.fetchRequests()
  recentRequests.value = requestsStore.requests
    .slice(0, 5)
    .map(request => ({
      ...request,
      manager: requestsStore.getManagerById(request.managerId)
    }))
})
</script>

<style scoped>
.dashboard-view {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.dashboard-title {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.title-icon {
  margin-right: 12px;
  color: var(--primary-color);
}

.quick-actions {
  display: flex;
  gap: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stats-icon {
  width: 24px;
  height: 24px;
}

.recent-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 1.2rem;
  margin-bottom: 16px;
  color: var(--text-secondary);
}

.mr-2 {
  margin-right: 8px;
}

.text-green-500 {
  color: #10b981;
}
</style>
