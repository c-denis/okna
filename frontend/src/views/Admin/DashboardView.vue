<template>
  <div class="admin-dashboard">
    <h1>Административная панель</h1>
    <div class="stats-grid">
      <StatsCard
        title="Пользователи"
        :value="usersCount"
        icon="👥"
        :trend="usersTrend"
      />
      <StatsCard
        title="Активные заявки"
        :value="activeRequests"
        icon="📋"
        :trend="requestsTrend"
        variant="warning"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import StatsCard from '@/components/features/Dashboard/StatsCard.vue'

const usersCount = ref(42)
const usersTrend = ref(5)
const activeRequests = ref(17)
const requestsTrend = ref(-2)
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
