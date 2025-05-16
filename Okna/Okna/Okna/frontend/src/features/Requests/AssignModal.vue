<template>
  <AppModal :show="true" @close="$emit('close')">
    <h2>Назначить заявку №{{ request.id }}</h2>
    <AppSelect
      v-model="selectedManager"
      :options="managerOptions"
      placeholder="Выберите менеджера"
    />
    <template #footer>
      <AppButton @click="$emit('close')">Отмена</AppButton>
      <AppButton
        type="primary"
        :disabled="!selectedManager"
        @click="handleAssign"
      >
        Назначить
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Manager } from '@/types/users';
import type { Request } from '@/types/requests';

const props = defineProps<{
  request: Request;
  managers: Manager[];
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'assign', managerId: string): void;
}>();

const selectedManager = ref<string | null>(null);

const managerOptions = computed(() => {
  return props.managers.map(m => ({
    value: m.id,
    text: `${m.name} (${m.specialization || 'Общий'})`
  }));
});

const handleAssign = () => {
  if (!selectedManager.value) {
    alert('Выберите менеджера');
    return;
  }
  emit('assign', selectedManager.value);
  emit('close');
};
</script>
