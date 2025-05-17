<template>
  <div class="reports-view">
    <h1>Отчеты</h1>

    <RequestFilters @filter="handleFilter" />

    <div class="report-period">
      <h2>Отчет за период: {{ periodText }}</h2>
    </div>

    <ReportView :data="reportData" />

    <div class="managers-section">
      <h2>Эффективность менеджеров</h2>
      <div class="managers-grid">
        <ManagerCard
          v-for="manager in managers"
          :key="manager.id"
          :manager="manager"
          :stats="getManagerStats(manager.id)"
          @select="showManagerDetails"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import RequestFilters from '@/components/RequestFilters.vue';
import reportsApi from '@/composables/api/reports.api';
import ReportView from '@/components/ReportView.vue';
import ManagerCard from '@/components/ManagerCard.vue';

const reportData = ref<ReportData | null>(null);
const isLoading = ref(false);

onMounted(async () => {
  isLoading.value = true;
  try {
    reportData.value = await reportsApi.fetchReports({
      period: 'week'
    });
  } finally {
    isLoading.value = false;
  }
});

const filters = ref({
  period: 'today',
  status: 'all',
  dateFrom: '',
  dateTo: ''
});

const managers = ref([
  { id: 1, name: 'Иванов И.', position: 'Мастер', status: 'free' },
  { id: 2, name: 'Петров П.', position: 'Мастер', status: 'busy' },
  { id: 3, name: 'Сидоров С.', position: 'Старший мастер', status: 'vacation' }
]);

const reportData = ref({
  total: 124,
  completed: 89,
  rejected: 12,
  averageTime: '2ч 15м'
});

const periodText = computed(() => {
  if (filters.value.period === 'today') return 'Сегодня';
  if (filters.value.period === 'week') return 'Текущая неделя';
  if (filters.value.period === 'month') return 'Текущий месяц';
  return `${filters.value.dateFrom} - ${filters.value.dateTo}`;
});

const handleFilter = (newFilters) => {
  filters.value = newFilters;
  // Здесь должен быть запрос к API для получения новых данных
  fetchReportData();
};

const getManagerStats = (managerId) => {
  // Заглушка - в реальном приложении данные должны приходить с сервера
  const stats = {
    1: { completed: 12, rejected: 2 },
    2: { completed: 8, rejected: 1 },
    3: { completed: 15, rejected: 0 }
  };
  return stats[managerId] || { completed: 0, rejected: 0 };
};

const showManagerDetails = (managerId) => {
  console.log('Selected manager:', managerId);
  // Навигация к деталям менеджера
};

const fetchReportData = async () => {
  // Запрос к API для получения данных отчетов
  // const response = await api.getReports(filters.value);
  // reportData.value = response.data;
};
</script>

<style scoped>
.reports-view {
  padding: 20px;
}

.report-period {
  margin: 20px 0;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.managers-section {
  margin-top: 40px;
}

.managers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .managers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
