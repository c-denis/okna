<script setup lang="ts">
import { useUsersStore } from '@/stores/user.store';
import { useRequestsStore } from '@/stores/requests.store';
import { computed } from 'vue';

const usersStore = useUsersStore();
const requestsStore = useRequestsStore();

// Заявки только для города руководителя
const cityRequests = computed(() => {
  if (!usersStore.currentUser?.city_id) return [];
  return requestsStore.requests.filter(
    r => r.city_id === usersStore.currentUser?.city_id
  );
});

// Статистика по статусам
const stats = computed(() => {
  return {
    total: cityRequests.value.length,
    completed: cityRequests.value.filter(r => r.status === 'completed').length,
    rejected: cityRequests.value.filter(r => r.status === 'rejected').length,
    inProgress: cityRequests.value.filter(r => r.status === 'in_progress').length
  };
});
</script>

<template>
  <div class="leader-dashboard">
    <h2>Заявки города #{{ usersStore.currentUser?.city_id }}</h2>

    <div class="stats">
      <div>Всего: {{ stats.total }}</div>
      <div>Выполнено: {{ stats.completed }}</div>
      <div>Отказов: {{ stats.rejected }}</div>
      <div>В работе: {{ stats.inProgress }}</div>
    </div>

    <RequestsTable :requests="cityRequests" />
  </div>
</template>

<style scoped>
.leader-dashboard {
  padding: 20px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 20px 0;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}
</style>
