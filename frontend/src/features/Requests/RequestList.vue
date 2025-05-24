<template>
  <div class="request-list-container">
    <!-- Секция фильтров -->
    <div class="filters-section">
      <AppInput
        v-model="filters.search"
        placeholder="Поиск по клиенту или адресу"
        icon="search"
        class="search-input"
      />

      <AppSelect
        v-model="filters.status"
        :options="statusOptions"
        placeholder="Все статусы"
        clearable
      />

      <AppSelect
        v-model="filters.city_id"
        :options="cityOptionsWithTypes"
        placeholder="Все города"
        clearable
      />

      <AppButton
        variant="outlined"
        @click="resetFilters"
      >
        Сбросить
      </AppButton>
    </div>

    <!-- Статус загрузки -->
    <div v-if="loading" class="status-message">
      <AppSpinner size="medium" />
      <span>Загрузка данных...</span>
    </div>

    <!-- Отображение ошибок -->
    <AppAlert
      v-else-if="error"
      type="error"
      :message="error"
      class="status-message"
    />

    <!-- Таблица заявок -->
    <AppTable
      v-else
      :headers="tableHeaders"
      :items="requestsAsRecordArray"
      :empty-message="emptyMessage"
      class="requests-table"
    >
      <template #cell-status="{ item }">
        <StatusBadge :status="item.status" />
        <span v-if="item.is_blacklisted" class="blacklist-badge">
          <AppIcon name="warning" color="error" size="small" />
          Чёрный список
        </span>
      </template>

      <template #cell-actions="{ item }">
        <div class="actions-cell">
          <AppButton
            v-if="canAssign(item)"
            size="small"
            variant="text"
            @click="openAssignModal(item)"
          >
            Назначить
          </AppButton>

          <AppButton
            size="small"
            variant="text"
            @click="openDetailsModal(item)"
          >
            Подробнее
          </AppButton>
        </div>
      </template>
    </AppTable>

    <AssignModal
      v-if="showAssignModal && selectedRequest"
      :request="selectedRequest"
      :managers="availableManagers"
      @close="showAssignModal = false"
      @assign="handleAssign"
    />

    <RequestDetailsModal
      v-if="showDetailsModal && selectedRequest"
      :request="selectedRequest"
      @close="showDetailsModal = false"
      @status-update="handleStatusUpdate"
      @blacklist="handleBlacklistPrompt"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRequestsStore } from '@/stores/requests.store'
import { useUsersStore } from '@/stores/user.store'
import { useAuthStore } from '@/stores/auth.store'
import { RequestStatus } from '@/types/requests'
import type { Request } from '@/types/requests'
import AssignModal from './AssignModal.vue'
import RequestDetailsModal from './RequestDetailsModal.vue'

// Инициализация хранилищ
const requestsStore = useRequestsStore()
const usersStore = useUsersStore()
const authStore = useAuthStore()

// Состояние компонента
const loading = computed(() => requestsStore.loading)
const error = computed(() => requestsStore.error)
const showAssignModal = ref(false)
const showDetailsModal = ref(false)
const selectedRequest = ref<Request>()

// Фильтры
const filters = computed({
  get: () => ({
    search: requestsStore.filters.search || '',
    status: requestsStore.filters.status,
    city_id: requestsStore.filters.city_id
  }),
  set: (value) => requestsStore.setFilters({
    search: value.search || '',
    status: value.status,
    city_id: value.city_id
  })
})

// Данные из хранилищ
const requests = computed(() => requestsStore.requests)
const availableManagers = computed(() => usersStore.availableManagers)
const userRole = computed(() => authStore.user?.role)

// Опции для фильтров
const statusOptions = [
  { value: undefined, label: 'Все статусы', disabled: false },
  { value: RequestStatus.UNASSIGNED, label: 'Не назначена', disabled: false },
  { value: RequestStatus.ASSIGNED, label: 'Назначена', disabled: false },
  { value: RequestStatus.IN_PROGRESS, label: 'В работе', disabled: false },
  { value: RequestStatus.COMPLETED, label: 'Завершена', disabled: false },
  { value: RequestStatus.REJECTED, label: 'Отказ', disabled: false }
]

const cityOptionsWithTypes = computed(() => {
  const cities = Array.from(
    new Set(requests.value.map(r => r.city).filter((city): city is string => !!city))
  )

  return [
    { value: undefined, label: 'Все города', disabled: false },
    ...cities.map(city => ({
      value: requestsStore.requests.find(r => r.city === city)?.city_id as number | undefined,
      label: city,
      disabled: false
    }))
  ]
})

// Заголовки таблицы
const tableHeaders: {
  text: string
  value: string
  width?: string
  align?: 'left' | 'right' | 'center'
}[] = [
  { text: 'ID', value: 'id', width: '80px', align: 'left' },
  { text: 'Клиент', value: 'client_name' },
  { text: 'Телефон', value: 'phone' },
  { text: 'Адрес', value: 'address' },
  { text: 'Статус', value: 'status', width: '180px' },
  { text: 'Дата создания', value: 'created_at', width: '150px' },
  { text: 'Действия', value: 'actions', width: '180px', align: 'right' }
]

const requestsAsRecordArray = computed(() =>
  requestsStore.filteredRequests.map(request => ({
    ...request,
    assigned_to: request.assigned_to ? {
      ...request.assigned_to,
      status: request.assigned_to.status as string
    } : undefined
  })) as Record<string, unknown>[]
)

const emptyMessage = computed(() => {
  if (Object.values(requestsStore.filters).some(Boolean)) {
    return 'Нет заявок, соответствующих фильтрам'
  }
  return 'Нет доступных заявок'
})

const fetchData = async () => {
  try {
    await Promise.all([
      requestsStore.fetchRequests(),
      userRole.value === 'coordinator' && usersStore.fetchManagers()
    ])
  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
  }
}

const canAssign = (request: Request) => {
  return userRole.value === 'coordinator' && request.status === RequestStatus.UNASSIGNED
}

const openAssignModal = (request: Request) => {
  selectedRequest.value = request
  showAssignModal.value = true
}

const openDetailsModal = (request: Request) => {
  selectedRequest.value = request
  showDetailsModal.value = true
}

const handleAssign = async (managerId: string) => {
  if (selectedRequest.value) {
    try {
      await requestsStore.assignRequest(selectedRequest.value.id, { manager_id: managerId })
      showAssignModal.value = false
    } catch (err) {
      console.error('Ошибка назначения:', err)
    }
  }
}

const handleStatusUpdate = async (status: RequestStatus, comment?: string) => {
  if (selectedRequest.value) {
    try {
      await requestsStore.updateRequestStatus(
        selectedRequest.value.id,
        status,
        comment
      )
      showDetailsModal.value = false
    } catch (err) {
      console.error('Ошибка обновления статуса:', err)
    }
  }
}

const handleBlacklistPrompt = async () => {
  if (!selectedRequest.value) return

  const reason = prompt('Введите причину добавления в черный список:')
  if (reason) {
    try {
      await requestsStore.addToBlacklist(selectedRequest.value.id, reason)
      showDetailsModal.value = false
    } catch (err) {
      console.error('Ошибка добавления в ЧС:', err)
    }
  }
}

const resetFilters = () => {
  requestsStore.resetFilters()
}

onMounted(fetchData)
</script>

<style scoped>
.request-list-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filters-section {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 250px;
  max-width: 400px;
}

.status-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
}

.requests-table {
  margin-top: 12px;
}

.blacklist-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  color: var(--color-error);
  font-size: 0.85rem;
}

.actions-cell {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
