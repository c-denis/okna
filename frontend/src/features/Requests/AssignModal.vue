<script setup lang="ts">
/**
 * МОДАЛЬНОЕ ОКНО НАЗНАЧЕНИЯ МЕНЕДЖЕРА НА ЗАЯВКУ
 *
 * Компонент позволяет выбрать доступного менеджера для выполнения заявки.
 * Интегрируется с хранилищами usersStore и requestsStore.
 */

import { ref, computed, onMounted } from 'vue'
import { useUsersStore } from '@/stores/user.store'
import { useRequestsStore } from '@/stores/requests.store'
import type { Request as ApiRequest } from '@/composables/api/requests.api'
import type { Request as TypeRequest, AssignRequestData } from '@/types/requests'
import { ManagerStatus } from '@/types/users'
import { RequestStatus } from '@/types/requests'

// Определяем интерфейс для параметров запроса менеджеров
interface FetchManagersParams {
  city_id?: number;
  status?: ManagerStatus;
}

// Определяем пропсы компонента
const props = defineProps<{
  /**
   * Объект заявки для назначения
   * Должен содержать обязательные поля:
   * - id: string - идентификатор заявки
   * - city_id: number - идентификатор города
   * - Адресные данные: street, house, building, apartment
   */
  request: TypeRequest
}>()

// Определяем события компонента
const emit = defineEmits<{
  /**
   * Событие закрытия модального окна
   */
  (e: 'close'): void

  /**
   * Событие успешного назначения менеджера
   * @param request - Обновленный объект заявки
   */
  (e: 'assigned', request: TypeRequest): void
}>()

// Инициализация хранилищ
const usersStore = useUsersStore()
const requestsStore = useRequestsStore()

// Реактивные состояния компонента
const selectedManagerId = ref<string | null>(null)
const loading = ref(false)
const assigning = ref(false)
const error = ref<string | null>(null)

/**
 * Загружает менеджеров при монтировании компонента
 */
onMounted(async () => {
  loading.value = true
  try {
    // Подготавливаем параметры запроса
    const params: FetchManagersParams = {
      city_id: props.request.city_id,
      status: ManagerStatus.AVAILABLE
    }
    await usersStore.fetchManagers(params)
  } catch (err) {
    error.value = 'Не удалось загрузить менеджеров'
    console.error('Error loading managers:', err)
  } finally {
    loading.value = false
  }
})

/**
 * Вычисляемое свойство - доступные для назначения менеджеры
 * Фильтрует по статусу AVAILABLE и текущей нагрузке
 */
const availableManagers = computed(() => {
  return usersStore.availableManagers.filter(m =>
    m.status === ManagerStatus.AVAILABLE &&
    m.current_assignments < m.max_assignments
  )
})

/**
 * Вычисляемое свойство - данные выбранного менеджера
 */
const selectedManager = computed(() => {
  return selectedManagerId.value
    ? usersStore.getManagerById(selectedManagerId.value)
    : null
})

/**
 * Обработчик назначения менеджера на заявку
 */
const handleAssign = async () => {
  if (!selectedManagerId.value || !selectedManager.value) {
    error.value = 'Выберите менеджера для назначения'
    return
  }

  assigning.value = true
  error.value = null

  try {
    // Подготавливаем данные для назначения
    const assignData: AssignRequestData = {
      manager_id: selectedManagerId.value
    }

    // Вызываем метод назначения из хранилища
    const updatedRequest = await requestsStore.assignRequest(
      props.request.id,
      assignData
    )

    // Обновляем статус менеджера
    await usersStore.updateManagerStatus(
      selectedManagerId.value,
      ManagerStatus.BUSY,
      props.request.id
    )

    // Преобразуем тип заявки для родительского компонента
    const typedRequest: TypeRequest = {
      ...props.request,
      ...updatedRequest,
      id: props.request.id,
      assigned_to: selectedManager.value,
      status: RequestStatus.ASSIGNED // ✅ Правильно
    }

    emit('assigned', typedRequest)
    emit('close')
  } catch (err) {
    error.value = err instanceof Error
      ? err.message
      : 'Произошла ошибка при назначении заявки'
    console.error('Assignment error:', err)
  } finally {
    assigning.value = false
  }
}
</script>

<template>
  <div class="assign-modal">
    <h3>Назначение заявки #{{ request.id }}</h3>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="loading" class="loading">
      Загрузка списка менеджеров...
    </div>

    <div v-else class="manager-selection">
      <label>Выберите менеджера:</label>
      <select
        v-model="selectedManagerId"
        :disabled="assigning"
      >
        <option :value="null">Не назначено</option>
        <option
          v-for="manager in availableManagers"
          :key="manager.id"
          :value="manager.id"
        >
          {{ manager.name }} ({{ manager.specialization || 'без специализации' }})
        </option>
      </select>
    </div>

    <div class="actions">
      <button
        @click="handleAssign"
        :disabled="!selectedManagerId || assigning"
      >
        {{ assigning ? 'Назначение...' : 'Назначить' }}
      </button>
      <button @click="emit('close')" :disabled="assigning">
        Отмена
      </button>
    </div>
  </div>
</template>

<style scoped>
.assign-modal {
  padding: 20px;
  background: white;
  border-radius: 8px;
  max-width: 500px;
  margin: 0 auto;
}

.error-message {
  color: red;
  margin-bottom: 15px;
}

.loading {
  padding: 10px;
  text-align: center;
}

.manager-selection {
  margin: 15px 0;
}

.manager-selection select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.actions button {
  padding: 8px 15px;
  cursor: pointer;
}
</style>
