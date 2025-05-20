<template>
  <AppModal
    :show="true"
    :loading="loading"
    @close="handleClose"
  >
    <template #header>
      <h2>Назначить заявку №{{ request.id }}</h2>
      <p class="client-info">{{ request.client_name }} - {{ request.address }}</p>
    </template>

    <div class="assign-content">
      <AppSelect
        v-model="selectedManagerId"
        :options="availableManagerOptions"
        placeholder="Выберите менеджера"
        :disabled="loading"
      />

      <div v-if="selectedManager" class="manager-info">
        <div class="manager-status">
          Статус:
          <StatusBadge :status="selectedManager.status" />
          <span v-if="selectedManager.status !== 'free'" class="assign-warning">
            (Может быть перегружен)
          </span>
        </div>
        <div class="manager-stats">
          Текущая нагрузка: {{ selectedManager.current_assignments }}/{{ selectedManager.max_assignments }}
        </div>
      </div>

      <AppAlert
        v-if="error"
        type="error"
        :message="error"
        class="error-alert"
      />
    </div>

    <template #footer>
      <AppButton @click="handleClose" :disabled="loading">
        Отмена
      </AppButton>
      <AppButton
        type="primary"
        :disabled="!canAssign || loading"
        :loading="assigning"
        @click="handleAssign"
      >
        {{ assignButtonText }}
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRequestsStore } from '@/stores/requests.store'
import { useManagersStore } from '@/stores/managers.store'
import type { Manager } from '@/types/users'
import type { Request } from '@/types/requests'

const props = defineProps<{
  request: Request
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'assigned', request: Request): void
}>()

const requestsStore = useRequestsStore()
const managersStore = useManagersStore()

const selectedManagerId = ref<number | null>(null)
const loading = ref(false)
const assigning = ref(false)
const error = ref<string | null>(null)

// Загружаем актуальный список менеджеров при открытии
loading.value = true
managersStore.fetchAvailableManagers()
  .catch(err => {
    error.value = 'Не удалось загрузить список менеджеров'
    console.error(err)
  })
  .finally(() => loading.value = false)

// Доступные для назначения менеджеры
const availableManagers = computed(() => {
  return managersStore.availableManagers.filter(m =>
    m.status !== 'dayoff' &&
    m.current_assignments < m.max_assignments
  )
})

// Опции для select
const availableManagerOptions = computed(() => {
  return availableManagers.value.map(m => ({
    value: m.id,
    text: `${m.name} (${m.specialization || 'Общий'}) - ${m.current_assignments}/${m.max_assignments}`,
    disabled: m.status !== 'free'
  }))
})

// Выбранный менеджер
const selectedManager = computed(() => {
  if (!selectedManagerId.value) return null
  return managersStore.availableManagers.find(m => m.id === selectedManagerId.value) || null
})

// Можно ли назначить
const canAssign = computed(() => {
  if (!selectedManager.value) return false
  return selectedManager.value.status === 'free' &&
    selectedManager.value.current_assignments < selectedManager.value.max_assignments
})

// Текст кнопки назначения
const assignButtonText = computed(() => {
  if (!selectedManager.value) return 'Назначить'
  return canAssign.value
    ? 'Назначить'
    : 'Менеджер недоступен'
})

// Обработка назначения
const handleAssign = async () => {
  if (!selectedManagerId.value || !canAssign.value) return

  assigning.value = true
  error.value = null

  try {
    const updatedRequest = await requestsStore.assignRequest(
      props.request.id,
      selectedManagerId.value
    )

    emit('assigned', updatedRequest)
    handleClose()

  } catch (err) {
    error.value = err instanceof Error
      ? err.message
      : 'Ошибка при назначении заявки'
    console.error('Assign error:', err)

  } finally {
    assigning.value = false
  }
}

// Закрытие модального окна
const handleClose = () => {
  if (!assigning.value) {
    emit('close')
  }
}

// Сбрасываем ошибку при смене менеджера
watch(selectedManagerId, () => {
  error.value = null
})
</script>

<style scoped>
.assign-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 12px 0;
}

.client-info {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 4px;
}

.manager-info {
  padding: 12px;
  background: var(--background-secondary);
  border-radius: 8px;
  font-size: 0.9rem;
}

.manager-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.assign-warning {
  color: var(--color-warning);
  font-size: 0.85rem;
}

.error-alert {
  margin-top: 12px;
}
</style>
