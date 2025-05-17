<template>
  <div class="report-view">
    <h2>Сводная статистика</h2>

    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.title">
        <h3>{{ stat.title }}</h3>
        <p class="stat-value">{{ stat.value }}</p>
        <p class="stat-change" :class="stat.trend">
          {{ stat.change }}% <span v-if="stat.trend === 'up'">↑</span>
          <span v-else-if="stat.trend === 'down'">↓</span>
        </p>
      </div>
    </div>

    <div class="charts">
      <div class="chart-container">
        <h3>Заявки по статусам</h3>
        <canvas ref="statusChart"></canvas>
      </div>
      <div class="chart-container">
        <h3>Заявки по городам</h3>
        <canvas ref="cityChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

const statusChart = ref(null);
const cityChart = ref(null);

const stats = ref([
  { title: 'Всего заявок', value: 124, change: 12, trend: 'up' },
  { title: 'Выполнено', value: 89, change: 5, trend: 'up' },
  { title: 'Отказов', value: 12, change: -3, trend: 'down' },
  { title: 'Среднее время', value: '2ч 15м', change: -10, trend: 'down' }
]);

onMounted(() => {
  renderCharts();
});

const renderCharts = () => {
  // Статусы заявок
  new Chart(statusChart.value, {
    type: 'doughnut',
    data: {
      labels: ['Новые', 'Назначенные', 'В работе', 'Завершенные', 'Отказы'],
      datasets: [{
        data: [15, 22, 18, 89, 12],
        backgroundColor: [
          '#FFC107',
          '#2196F3',
          '#4CAF50',
          '#607D8B',
          '#F44336'
        ]
      }]
    }
  });

  // Заявки по городам
  new Chart(cityChart.value, {
    type: 'bar',
    data: {
      labels: ['Москва', 'СПб', 'Казань', 'Екатеринбург', 'Новосибирск'],
      datasets: [{
        label: 'Заявки',
        data: [45, 32, 18, 15, 14],
        backgroundColor: '#2196F3'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
};
</script>

<style scoped>
.report-view {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin: 20px 0;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 8px 0;
}

.stat-change {
  font-size: 0.9rem;
}

.stat-change.up {
  color: #4CAF50;
}

.stat-change.down {
  color: #F44336;
}

.charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 30px;
}

.chart-container {
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .charts {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
