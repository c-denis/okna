<template>
  <div class="report-view">
    <div class="report-header">
      <h2>Отчеты по заявкам</h2>

      <div class="report-filters">
        <AppSelect
          v-model="period"
          :options="periodOptions"
          label="Период"
          class="filter-select"
        />

        <AppDatePicker
          v-if="period === 'custom'"
          v-model="customDates"
          range
          placeholder="Выберите даты"
          class="filter-datepicker"
        />

        <AppSelect
          v-model="selectedCity"
          :options="cityOptions"
          label="Город"
          clearable
          class="filter-select"
        />

        <AppButton
          @click="exportToExcel"
          variant="outlined"
          icon="download"
        >
          Экспорт
        </AppButton>
      </div>
    </div>

    <!-- Статистические карточки -->
    <div class="stats-grid">
      <StatCard
        title="Всего заявок"
        :value="reportData?.total_orders || 0"
        :change="reportData?.order_change_percent || 0"
        icon="assignment"
      />

      <StatCard
        title="Выполнено"
        :value="reportData?.completed_orders || 0"
        :change="reportData?.completed_change_percent || 0"
        icon="check_circle"
        color="success"
      />

      <StatCard
        title="Отказы"
        :value="reportData?.rejected_orders || 0"
        :change="reportData?.rejected_change_percent || 0"
        icon="cancel"
        color="error"
      />

      <StatCard
        title="Среднее время"
        :value="formatDuration(reportData?.avg_completion_time)"
        :change="reportData?.time_change_percent || 0"
        icon="schedule"
        color="info"
      />
    </div>

    <!-- Основные графики -->
    <div class="charts-section">
      <div class="chart-container">
        <div class="chart-header">
          <h3>Распределение по статусам</h3>
          <AppSelect
            v-model="statusChartType"
            :options="chartTypeOptions"
            size="small"
          />
        </div>
        <canvas ref="statusChart"></canvas>
      </div>

      <div class="chart-container">
        <div class="chart-header">
          <h3>Заявки по городам</h3>
          <AppSelect
            v-model="cityChartType"
            :options="chartTypeOptions"
            size="small"
          />
        </div>
        <canvas ref="cityChart"></canvas>
      </div>
    </div>

    <!-- Таблица с детализацией -->
    <div class="details-section">
      <h3>Детализация по менеджерам</h3>
      <AppTable
        :headers="managerHeaders"
        :items="reportData?.managers_stats || []"
        :loading="loading"
        class="manager-table"
      >
        <template #cell-efficiency="{ item }">
          <AppProgress
            :value="item.efficiency"
            :max="100"
            show-value
            :color="getEfficiencyColor(item.efficiency)"
          />
        </template>

        <template #cell-actions="{ item }">
          <AppButton
            size="small"
            variant="text"
            @click="showManagerDetails(item.id)"
          >
            Детали
          </AppButton>
        </template>
      </AppTable>
    </div>

    <!-- Модальное окно с детализацией по менеджеру -->
    <ManagerReportModal
      v-if="selectedManager"
      :manager-id="selectedManager"
      :period="activePeriod"
      @close="selectedManager = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useReportsStore } from '@/stores/reports.store'
import { useLocationsStore } from '@/stores/locations.store'
import { Chart } from 'chart.js/auto'
import { exportToExcel } from '@/utils/exporter'
import StatCard from '@/components/reports/StatCard.vue'
import ManagerReportModal from '@/components/reports/ManagerReportModal.vue'

// Сторы
const reportsStore = useReportsStore()
const locationsStore = useLocationsStore()

// Реактивные данные
const period = ref('week')
const customDates = ref([])
const selectedCity = ref(null)
const statusChart = ref(null)
const cityChart = ref(null)
const statusChartType = ref('doughnut')
const cityChartType = ref('bar')
const loading = ref(false)
const selectedManager = ref(null)

// Опции фильтров
const periodOptions = [
  { value: 'today', label: 'Сегодня' },
  { value: 'week', label: 'Неделя' },
  { value: 'month', label: 'Месяц' },
  { value: 'quarter', label: 'Квартал' },
  { value: 'year', label: 'Год' },
  { value: 'custom', label: 'Произвольный период' }
]

const chartTypeOptions = [
  { value: 'bar', label: 'Гистограмма' },
  { value: 'doughnut', label: 'Кольцевая' },
  { value: 'pie', label: 'Круговая' },
  { value: 'line', label: 'Линейная' }
]

const managerHeaders = [
  { text: 'Менеджер', value: 'name' },
  { text: 'Заявок', value: 'total_orders' },
  { text: 'Выполнено', value: 'completed' },
  { text: 'Отказов', value: 'rejected' },
  { text: 'Эффективность', value: 'efficiency' },
  { text: 'Действия', value: 'actions', align: 'right' }
]

// Вычисляемые свойства
const activePeriod = computed(() => {
  if (period.value !== 'custom') return period.value

  return {
    start: customDates.value[0],
    end: customDates.value[1]
  }
})

const cityOptions = computed(() => {
  return locationsStore.cities.map(city => ({
    value: city.id,
    label: city.name
  }))
})

const reportData = computed(() => reportsStore.currentReport)

// Инициализация данных
onMounted(async () => {
  await locationsStore.fetchCities()
  fetchReportData()
})

// Отслеживание изменений фильтров
watch([period, customDates, selectedCity], () => {
  fetchReportData()
}, { deep: true })

// Методы
const fetchReportData = async () => {
  loading.value = true

  try {
    await reportsStore.fetchReport({
      period: activePeriod.value,
      city_id: selectedCity.value
    })

    renderCharts()
  } catch (error) {
    console.error('Ошибка загрузки отчета:', error)
  } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  // Уничтожаем предыдущие графики
  if (statusChart.value?.chart) statusChart.value.chart.destroy()
  if (cityChart.value?.chart) cityChart.value.chart.destroy()

  // Данные для графиков
  const statusData = reportData.value?.status_stats || []
  const cityData = reportData.value?.city_stats || []

  // График статусов
  if (statusChart.value) {
    statusChart.value.chart = new Chart(statusChart.value, {
      type: statusChartType.value,
      data: {
        labels: statusData.map(s => s.status_name),
        datasets: [{
          label: 'Заявки',
          data: statusData.map(s => s.count),
          backgroundColor: [
            '#FFC107', // Новые
            '#2196F3', // Назначенные
            '#4CAF50', // В работе
            '#607D8B', // Завершенные
            '#F44336'  // Отказы
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'right'
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const total = context.dataset.data.reduce((a, b) => a + b, 0)
                const value = context.raw
                const percentage = Math.round((value / total) * 100)
                return `${context.label}: ${value} (${percentage}%)`
              }
            }
          }
        }
      }
    })
  }

  // График по городам
  if (cityChart.value) {
    cityChart.value.chart = new Chart(cityChart.value, {
      type: cityChartType.value,
      data: {
        labels: cityData.map(c => c.city_name),
        datasets: [{
          label: 'Заявки',
          data: cityData.map(c => c.count),
          backgroundColor: '#2196F3',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                const total = cityData.reduce((sum, item) => sum + item.count, 0)
                const percentage = Math.round((context.raw / total) * 100)
                return `${context.label}: ${context.raw} (${percentage}%)`
              }
            }
          }
        }
      }
    })
  }
}

const formatDuration = (seconds) => {
  if (!seconds) return '0ч 0м'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}ч ${minutes}м`
}

const getEfficiencyColor = (value) => {
  if (value >= 90) return 'success'
  if (value >= 70) return 'warning'
  return 'error'
}

const showManagerDetails = (managerId) => {
  selectedManager.value = managerId
}

const exportToExcel = () => {
  if (!reportData.value) return

  const data = [
    ['Отчет по заявкам', `Период: ${periodOptions.find(p => p.value === period.value)?.label}`],
    [],
    ['Всего заявок', reportData.value.total_orders],
    ['Выполнено', reportData.value.completed_orders],
    ['Отказов', reportData.value.rejected_orders],
    ['Среднее время выполнения', formatDuration(reportData.value.avg_completion_time)],
    [],
    ['Статус', 'Количество'],
    ...(reportData.value.status_stats?.map(s => [s.status_name, s.count]) || []),
    [],
    ['Город', 'Количество'],
    ...(reportData.value.city_stats?.map(c => [c.city_name, c.count]) || []),
    [],
    ['Менеджер', 'Всего', 'Выполнено', 'Отказов', 'Эффективность'],
    ...(reportData.value.managers_stats?.map(m => [
      m.name,
      m.total_orders,
      m.completed,
      m.rejected,
      `${m.efficiency}%`
    ]) || [])
  ]

  exportToExcel(data, `Отчет_${new Date().toISOString().slice(0,10)}`)
}

// Очистка при размонтировании
onBeforeUnmount(() => {
  if (statusChart.value?.chart) statusChart.value.chart.destroy()
  if (cityChart.value?.chart) cityChart.value.chart.destroy()
})
</script>

<style scoped>
.report-view {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.report-filters {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-select {
  min-width: 180px;
}

.filter-datepicker {
  min-width: 250px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-container {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 16px;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.details-section {
  margin-top: 24px;
}

.manager-table {
  margin-top: 16px;
}

@media (max-width: 1200px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .report-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .report-filters {
    width: 100%;
  }

  .filter-select,
  .filter-datepicker {
    width: 100%;
  }
}
</style>
