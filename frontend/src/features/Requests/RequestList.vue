<template>
  <div v-if="loading" class="loading">Загрузка...</div>
  <div v-else-if="error" class="error">{{ error }}</div>
  <div v-else class="request-list">
    <!-- Фильтры и поиск -->
    <div class="filters">
      <AppInput
        v-model="searchQuery"
        placeholder="Поиск по клиенту или адресу"
        class="search-input"
      />
      <AppSelect
        v-model="selectedStatus"
        :options="statusOptions"
        placeholder="Все статусы"
      />
      <AppSelect
        v-model="selectedCity"
        :options="cityOptions"
        placeholder="Все города"
      />
      <AppButton @click="resetFilters">Сбросить</AppButton>
    </div>

    <!-- Таблица заявок -->
    <AppTable :headers="headers" :items="filteredRequests">
      <template #cell-status="{ item }">
        <StatusBadge :status="item.status" />
        <span v-if="item.isBlacklisted" class="blacklist-indicator"> (ЧС)</span>
      </template>
      <template #cell-actions="{ item }">
        <div class="actions">
          <AppButton
            v-if="userRole === 'coordinator' && item.status === 'unassigned'"
            size="small"
            @click="openAssignModal(item)"
          >
            Назначить
          </AppButton>
          <AppButton
            v-if="
              (userRole === 'manager' && item.status === 'assigned') ||
              userRole === 'coordinator'
            "
            size="small"
            @click="openDetailsModal(item)"
          >
            Детали
          </AppButton>
        </div>
      </template>
    </AppTable>

    <!-- Модальное окно назначения -->
    <AssignModal
      v-if="showAssignModal"
      :request="selectedRequest"
      :managers="availableManagers"
      @close="showAssignModal = false"
      @assign="handleAssign"
    />

    <!-- Модальное окно деталей -->
    <RequestDetailsModal
      v-if="showDetailsModal"
      :request="selectedRequest"
      @close="showDetailsModal = false"
      @update-status="handleStatusUpdate"
      @blacklist="handleBlacklist"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useRequestsStore } from '@/stores/requests.store';
import { useUsersStore } from '@/stores/users.store';
import { useAuthStore } from '@/stores/auth.store';
import type { Request, RequestStatus } from '@/types/requests';
import type { Manager } from '@/types/users';

// Сторы
const requestsStore = useRequestsStore();
const usersStore = useUsersStore();
const authStore = useAuthStore();

// Состояние
const loading = ref(false);
const error = ref<string | null>(null);
const searchQuery = ref('');
const selectedStatus = ref<RequestStatus | 'all'>('all');
const selectedCity = ref<string>('all');
const showAssignModal = ref(false);
const showDetailsModal = ref(false);
const selectedRequest = ref<Request | null>(null);

// Заголовки таблицы
const headers = [
  { text: 'ID', value: 'id' },
  { text: 'Клиент', value: 'clientName' },
  { text: 'Телефон', value: 'phone' },
  { text: 'Адрес', value: 'address' },
  { text: 'Статус', value: 'status' },
  { text: 'Дата', value: 'createdAt' },
  { text: 'Действия', value: 'actions' },
];

// Опции фильтров
const statusOptions = [
  { value: 'all', text: 'Все статусы' },
  { value: 'unassigned', text: 'Не назначена' },
  { value: 'assigned', text: 'Назначена' },
  { value: 'in_progress', text: 'В работе' },
  { value: 'completed', text: 'Исполнена' },
  { value: 'rejected', text: 'Отказ' },
];

// Computed свойства
const userRole = computed(() => authStore.user?.role);
const allRequests = computed(() => requestsStore.requests);
const cityOptions = computed(() => {
  const cities = new Set(allRequests.value.map(r => r.city));
  return [{ value: 'all', text: 'Все города' }, ...Array.from(cities).map(c => ({ value: c, text: c }))];
});

const availableManagers = computed(() => {
  return usersStore.managers.filter(m => m.status === 'available');
});

const filteredRequests = computed(() => {
  return allRequests.value.filter(request => {
    const matchesSearch =
      request.clientName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      request.address.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesStatus =
      selectedStatus.value === 'all' || request.status === selectedStatus.value;

    const matchesCity =
      selectedCity.value === 'all' || request.city === selectedCity.value;

    return matchesSearch && matchesStatus && matchesCity;
  });
});

// Методы
const fetchData = async () => {
  loading.value = true;
  error.value = null;
  try {
    await requestsStore.fetchRequests();
    if (userRole.value === 'coordinator') {
      await usersStore.fetchManagers();
    }
  } catch (err) {
    error.value = 'Ошибка загрузки данных';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openAssignModal = (request: Request) => {
  selectedRequest.value = request;
  showAssignModal.value = true;
};

const openDetailsModal = (request: Request) => {
  selectedRequest.value = request;
  showDetailsModal.value = true;
};

const handleAssign = (managerId: string) => {
  if (selectedRequest.value) {
    requestsStore.assignRequest(selectedRequest.value.id, managerId);
    showAssignModal.value = false;
  }
};

const handleStatusUpdate = (status: RequestStatus) => {
  if (selectedRequest.value) {
    requestsStore.updateRequestStatus(selectedRequest.value.id, status);
    showDetailsModal.value = false;
  }
};

const handleBlacklist = () => {
  if (selectedRequest.value) {
    requestsStore.blacklistRequest(selectedRequest.value.id);
    showDetailsModal.value = false;
  }
};

const resetFilters = () => {
  searchQuery.value = '';
  selectedStatus.value = 'all';
  selectedCity.value = 'all';
};

// Хуки жизненного цикла
onMounted(fetchData);
</script>

<style scoped>
.request-list {
  padding: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 300px;
}

.actions {
  display: flex;
  gap: 8px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #d32f2f;
}

.blacklist-indicator {
  color: #f44336;
  font-weight: bold;
  margin-left: 4px;
}
</style>
