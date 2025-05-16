<template>
  <AppModal :show="true" @close="$emit('close')">
    <h2>Детали заявки №{{ request.id }}</h2>

    <div class="request-details">
      <div class="detail-row">
        <span class="detail-label">Клиент:</span>
        <span>{{ request.clientName }}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Телефон:</span>
        <span>{{ request.phone }}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Адрес:</span>
        <span>{{ fullAddress }}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Статус:</span>
        <StatusBadge :status="request.status" />
      </div>
      <div class="detail-row" v-if="request.managerId">
        <span class="detail-label">Менеджер:</span>
        <span>{{ assignedManager?.name || 'Не назначен' }}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Дата создания:</span>
        <span>{{ formattedDate }}</span>
      </div>
      <div class="detail-row" v-if="request.comment">
        <span class="detail-label">Комментарий:</span>
        <span>{{ request.comment }}</span>
      </div>
    </div>

    <div class="status-actions" v-if="canChangeStatus">
      <AppSelect
        v-model="selectedStatus"
        :options="availableStatusOptions"
        placeholder="Изменить статус"
      />
      <AppButton
        type="primary"
        :disabled="!selectedStatus"
        @click="handleStatusChange"
      >
        Обновить
      </AppButton>
    </div>

    <template #footer>
      <AppButton
        v-if="canBlacklist && !request.isBlacklisted"
        type="danger"
        @click="$emit('blacklist')"
      >
        В черный список
      </AppButton>
      <AppButton @click="$emit('close')">Закрыть</AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUsersStore } from '@/stores/users.store';
import { useAuthStore } from '@/stores/auth.store';
import type { Request, RequestStatus } from '@/types/requests';
import { format } from 'date-fns';

const props = defineProps<{
  request: Request;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'update-status', status: RequestStatus): void;
  (e: 'blacklist'): void;
}>();

const authStore = useAuthStore();
const usersStore = useUsersStore();
const selectedStatus = ref<RequestStatus | null>(null);

const fullAddress = computed(() => {
  return `${props.request.city}, ${props.request.address}`;
});

const formattedDate = computed(() => {
  return format(new Date(props.request.createdAt), 'dd.MM.yyyy HH:mm');
});

const assignedManager = computed(() => {
  return usersStore.managers.find(m => m.id === props.request.managerId);
});

const canChangeStatus = computed(() => {
  return ['coordinator', 'manager'].includes(authStore.user?.role || '');
});

const canBlacklist = computed(() => {
  return authStore.user?.role === 'coordinator';
});

const availableStatusOptions = computed(() => {
  const options = [];

  if (props.request.status === 'assigned') {
    options.push({ value: 'in_progress', text: 'В работе' });
    options.push({ value: 'rejected', text: 'Отказ' });
  }

  if (props.request.status === 'in_progress') {
    options.push({ value: 'completed', text: 'Исполнена' });
    options.push({ value: 'rejected', text: 'Отказ' });
  }

  return options;
});

const handleStatusChange = () => {
  if (selectedStatus.value) {
    emit('update-status', selectedStatus.value);
    emit('close');
  }
};
</script>

<style scoped>
.request-details {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 12px 16px;
  margin-bottom: 20px;
}

.detail-label {
  font-weight: 500;
  color: #666;
}

.status-actions {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}
</style>
