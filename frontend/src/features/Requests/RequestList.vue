<template>
  <div class="request-list-container">
    <!-- Фильтры -->
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
        v-model="filters.city"
        :options="cityOptions"
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

    <!-- Статус загрузки/ошибки -->
    <div v-if="loading" class="status-message">
      <AppSpinner size="medium" />
      <span>Загрузка данных...</span>
    </div>

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
      :items="filteredRequests"
      :empty-message="emptyMessage"
      class="requests-table"
    >
      <!-- Слот для статуса с цветовой индикацией -->
      <template #cell-status="{ item }">
        <StatusBadge :status="item.status" />
        <span v-if="item.is_blacklisted" class="blacklist-badge">
          <AppIcon name="warning" color="error" size="small" />
          Чёрный список
        </span>
      </template>

      <!-- Слот для действий -->
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

    <!-- Модальное окно назначения -->
    <AssignModal
      v-if="showAssignModal"
      :request="selectedRequest!"
      :managers="availableManagers"
      @close="showAssignModal = false"
      @assign="handleAssign"
    />

    <!-- Модальное окно деталей -->
    <RequestDetailsModal
      v-if="showDetailsModal"
      :request="selectedRequest!"
      @close="showDetailsModal = false"
      @status-update="handleStatusUpdate"
      @blacklist="handleBlacklist"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useRequestsStore } from '@/stores/requests.store';
import { useUsersStore } from '@/stores/users.store';
import { useAuthStore } from '@/stores/auth.store';
import { RequestStatus } from '@/types/requests';
import AssignModal from './AssignModal.vue';
import RequestDetailsModal from './RequestDetailsModal.vue';

// Сторы
const requestsStore = useRequestsStore();
const usersStore = useUsersStore();
const authStore = useAuthStore();

// Состояние
const loading = computed(() => requestsStore.loading);
const error = computed(() => requestsStore.error);
const showAssignModal = ref(false);
const showDetailsModal = ref(false);
const selectedRequest = ref<Request | null>(null);

// Фильтры
const filters = computed({
  get: () => requestsStore.filters,
  set: (value) => requestsStore.setFilters(value)
});

// Данные
const requests = computed(() => requestsStore.requests);
const filteredRequests = computed(() => requestsStore.filteredRequests);
const availableManagers = computed(() => usersStore.availableManagers);
const userRole = computed(() => authStore.user?.role);

// Опции фильтров
const statusOptions = [
  { value: undefined, label: 'Все статусы' },
  { value: RequestStatus.UNASSIGNED, label: 'Не назначена' },
  { value: RequestStatus.ASSIGNED, label: 'Назначена' },
  { value: RequestStatus.IN_PROGRESS, label: 'В работе' },
  { value: RequestStatus.COMPLETED, label: 'Завершена' },
  { value: RequestStatus.REJECTED, label: 'Отказ' }
];

const cityOptions = computed(() => {
  const cities = Array.from(new Set(requests.value.map(r => r.city).filter(Boolean));
  return [
    { value: undefined, label: 'Все города' },
    ...cities.map(city => ({ value: city, label: city }))
  ];
});

// Заголовки таблицы
const tableHeaders = [
  { key: 'id', label: 'ID', width: '80px' },
  { key: 'client_name', label: 'Клиент' },
  { key: 'phone', label: 'Телефон' },
  { key: 'address', label: 'Адрес' },
  { key: 'status', label: 'Статус', width: '180px' },
  { key: 'created_at', label: 'Дата создания', width: '150px' },
  { key: 'actions', label: 'Действия', width: '180px', align: 'right' }
];

const emptyMessage = computed(() => {
  if (Object.values(filters.value).some(Boolean)) {
    return 'Нет заявок, соответствующих фильтрам';
  }
  return 'Нет доступных заявок';
});

// Методы
const fetchData = async () => {
  try {
    await Promise.all([
      requestsStore.fetchRequests(),
      userRole.value === 'coordinator' && usersStore.fetchManagers()
    ]);
  } catch (err) {
    console.error('Ошибка загрузки данных:', err);
  }
};

const canAssign = (request: Request) => {
  return userRole.value === 'coordinator' && request.status === RequestStatus.UNASSIGNED;
};

const openAssignModal = (request: Request) => {
  selectedRequest.value = request;
  showAssignModal.value = true;
};

const openDetailsModal = (request: Request) => {
  selectedRequest.value = request;
  showDetailsModal.value = true;
};

const handleAssign = async (managerId: number) => {
  if (selectedRequest.value) {
    try {
      await requestsStore.assignRequest(selectedRequest.value.id, managerId);
      showAssignModal.value = false;
    } catch (err) {
      console.error('Ошибка назначения:', err);
    }
  }
};

const handleStatusUpdate = async (status: RequestStatus, comment?: string) => {
  if (selectedRequest.value) {
    try {
      await requestsStore.updateRequestStatus(
        selectedRequest.value.id,
        status,
        comment
      );
      showDetailsModal.value = false;
    } catch (err) {
      console.error('Ошибка обновления статуса:', err);
    }
  }
};

const handleBlacklist = async (reason: string) => {
  if (selectedRequest.value) {
    try {
      await requestsStore.addToBlacklist(selectedRequest.value.id, reason);
      showDetailsModal.value = false;
    } catch (err) {
      console.error('Ошибка добавления в ЧС:', err);
    }
  }
};

const resetFilters = () => {
  requestsStore.resetFilters();
};

// Хуки жизненного цикла
onMounted(fetchData);
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
