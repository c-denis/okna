<template>
  <div class="request-filters">
    <div class="filter-group">
      <label>Период:</label>
      <select v-model="selectedPeriod" @change="updateFilters">
        <option value="today">Сегодня</option>
        <option value="week">Неделя</option>
        <option value="month">Месяц</option>
        <option value="custom">Произвольный</option>
      </select>
    </div>

    <div class="filter-group" v-if="selectedPeriod === 'custom'">
      <label>С:</label>
      <input type="date" v-model="dateFrom" @change="updateFilters">
      <label>По:</label>
      <input type="date" v-model="dateTo" @change="updateFilters">
    </div>

    <div class="filter-group">
      <label>Статус:</label>
      <select v-model="selectedStatus" @change="updateFilters">
        <option value="all">Все</option>
        <option value="new">Новые</option>
        <option value="assigned">Назначенные</option>
        <option value="in_progress">В работе</option>
        <option value="completed">Завершенные</option>
        <option value="rejected">Отказы</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['filter']);

const selectedPeriod = ref('today');
const selectedStatus = ref('all');
const dateFrom = ref('');
const dateTo = ref('');

const updateFilters = () => {
  emit('filter', {
    period: selectedPeriod.value,
    status: selectedStatus.value,
    dateFrom: dateFrom.value,
    dateTo: dateTo.value
  });
};

// Установка дат по умолчанию для периода
watch(selectedPeriod, (newVal) => {
  const today = new Date();

  if (newVal === 'today') {
    dateFrom.value = today.toISOString().split('T')[0];
    dateTo.value = today.toISOString().split('T')[0];
  } else if (newVal === 'week') {
    const firstDay = new Date(today.setDate(today.getDate() - today.getDay()));
    dateFrom.value = firstDay.toISOString().split('T')[0];
    dateTo.value = new Date().toISOString().split('T')[0];
  } else if (newVal === 'month') {
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    dateFrom.value = firstDay.toISOString().split('T')[0];
    dateTo.value = new Date().toISOString().split('T')[0];
  }

  if (newVal !== 'custom') {
    updateFilters();
  }
}, { immediate: true });
</script>

<style scoped>
.request-filters {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

label {
  font-weight: 500;
}

select, input {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>
