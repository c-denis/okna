<template>
  <span :class="['status-badge', status]">
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { RequestStatus } from '@/types/requests';

const props = defineProps<{
  status: RequestStatus;
}>();

const statusText = computed(() => {
  const texts: Record<RequestStatus, string> = {
    unassigned: 'Не назначена',
    assigned: 'Назначена',
    in_progress: 'В работе',
    completed: 'Исполнена',
    rejected: 'Отказ'
  };
  return texts[props.status];
});
</script>

<style scoped>
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  display: inline-block;
}

.unassigned {
  background-color: #ffebee;
  color: #d32f2f;
}

.assigned {
  background-color: #e3f2fd;
  color: #1976d2;
}

.in_progress {
  background-color: #e8f5e9;
  color: #388e3c;
}

.completed {
  background-color: #f1f8e9;
  color: #689f38;
}

.rejected {
  background-color: #fbe9e7;
  color: #e64a19;
}
</style>
