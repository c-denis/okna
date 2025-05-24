<template>
  <form @submit.prevent="handleSubmit" class="request-form">
    <!-- Секция данных клиента -->
    <div class="form-section">
      <h3 class="section-title">Данные клиента</h3>
      <div class="form-grid">
        <!-- Поле ФИО клиента -->
        <AppInput
          v-model="form.client_name"
          label="ФИО клиента*"
          required
          :error="errors.client_name"
          @blur="validateField('client_name')"
        />

        <!-- Поле телефона с маской -->
        <AppInput
          v-model="form.phone"
          label="Телефон*"
          required
          mask="+7 (###) ###-##-##"
          :error="errors.phone"
          @blur="validatePhone"
        />
      </div>
    </div>

    <!-- Секция адреса -->
    <div class="form-section">
      <h3 class="section-title">Адрес</h3>
      <div class="form-grid">
        <!-- Выбор города -->
        <AppSelect
          v-model="form.city"
          label="Город*"
          :options="cityOptions"
          required
          :error="errors.city"
          @blur="validateField('city')"
          @update:modelValue="fetchStreets"
        />

        <!-- Поле улицы -->
        <AppInput
          v-model="form.street"
          label="Улица*"
          required
          :error="errors.street"
          @blur="validateField('street')"
        />

        <!-- Группа полей адреса -->
        <div class="address-row">
          <AppInput
            v-model="form.house"
            label="Дом*"
            required
            class="address-input"
            :error="errors.house"
            @blur="validateField('house')"
          />

          <AppInput
            v-model="form.building"
            label="Корпус"
            class="address-input"
          />

          <AppInput
            v-model="form.apartment"
            label="Квартира"
            class="address-input"
          />
        </div>
      </div>
    </div>

    <!-- Секция дополнительной информации -->
    <div class="form-section">
      <h3 class="section-title">Дополнительно</h3>
      <!-- Поле комментария -->
      <AppTextarea
        v-model="form.comment"
        label="Комментарий"
        placeholder="Опишите проблему"
        rows="3"
      />

      <!-- Выбор приоритета -->
      <AppSelect
        v-model="form.priority"
        label="Приоритет"
        :options="priorityOptions"
      />
    </div>

    <!-- Блок ошибок формы -->
    <div v-if="error" class="form-error">
      <AppAlert type="error" :message="error" />
    </div>

    <!-- Кнопки действий формы -->
    <div class="form-actions">
      <AppButton
        type="primary"
        :loading="loading"
        :disabled="!isFormValid"
      >
        {{ editMode ? 'Обновить заявку' : 'Создать заявку' }}
      </AppButton>

      <AppButton
        v-if="editMode"
        variant="outlined"
        @click="resetForm"
      >
        Отменить
      </AppButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRequestsStore } from '@/stores/requests.store'
import { useLocationsStore } from '@/stores/locations.store'
import { useValidation } from '@/composables/useValidation'
import type { Request, RequestCreateData } from '@/types/requests'

/**
 * Пропсы компонента:
 * - initialData: Данные для редактирования существующей заявки
 */
const props = defineProps<{
  initialData?: Request | null
}>()

/**
 * События компонента:
 * - success: Успешное сохранение формы
 * - cancel: Отмена редактирования
 */
const emit = defineEmits<{
  (e: 'success'): void
  (e: 'cancel'): void
}>()

// Инициализация хранилищ
const requestsStore = useRequestsStore()
const locationsStore = useLocationsStore()

// Состояние формы
const form = ref<Omit<RequestCreateData, 'address' | 'city_id'> & {
  city: string
  street: string
  house: string
  building: string
  apartment: string
}>({
  client_name: '',
  phone: '',
  city: '',
  street: '',
  house: '',
  building: '',
  apartment: '',
  comment: '',
  priority: 'medium'
})

const loading = ref(false)
const error = ref<string | null>(null)

// Правила валидации полей формы
const { errors, validateField, validateForm, resetValidation } = useValidation(
  form,
  {
    client_name: { required: true, minLength: 3 },
    phone: { required: true, pattern: /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/ },
    city: { required: true },
    street: { required: true },
    house: { required: true }
  }
)

// Опции для выпадающих списков
const priorityOptions = [
  { value: 'low', label: 'Низкий' },
  { value: 'medium', label: 'Средний' },
  { value: 'high', label: 'Высокий' }
]

const cityOptions = computed(() => {
  return locationsStore.cities.map(city => ({
    value: city.name,
    label: city.name
  }))
})

// Вычисляемые свойства
const editMode = computed(() => !!props.initialData)
const isFormValid = computed(() => {
  return (
    form.value.client_name &&
    form.value.phone &&
    form.value.city &&
    form.value.street &&
    form.value.house &&
    !loading.value
  )
})

/**
 * Валидация номера телефона с кастомным сообщением об ошибке
 */
const validatePhone = () => {
  validateField('phone')
  if (errors.value.phone) {
    errors.value.phone = 'Введите корректный номер телефона'
  }
}

/**
 * Загрузка улиц для выбранного города
 */
const fetchStreets = async (city: string) => {
  if (city) {
    await locationsStore.fetchStreets(city)
  }
}

/**
 * Сброс формы к начальным значениям
 */
const resetForm = () => {
  if (props.initialData) {
    initForm()
  } else {
    form.value = {
      client_name: '',
      phone: '',
      city: '',
      street: '',
      house: '',
      building: '',
      apartment: '',
      comment: '',
      priority: 'medium'
    }
  }
  resetValidation()
  error.value = null
}

/**
 * Инициализация формы данными для редактирования
 */
const initForm = () => {
  if (props.initialData) {
    const { client_name, phone, address, comment, priority } = props.initialData
    form.value = {
      client_name,
      phone,
      comment: comment || '',
      priority: priority || 'medium',
      ...parseAddress(address)
    }
  }
}

/**
 * Парсинг адреса из строки в объект
 */
const parseAddress = (address: string) => {
  const result = {
    city: '',
    street: '',
    house: '',
    building: '',
    apartment: ''
  }

  const parts = address.split(', ')
  parts.forEach(part => {
    if (part.startsWith('г.')) {
      result.city = part.replace('г. ', '')
    } else if (part.startsWith('ул.')) {
      result.street = part.replace('ул. ', '')
    } else if (part.startsWith('д.')) {
      result.house = part.replace('д. ', '')
    } else if (part.startsWith('к.')) {
      result.building = part.replace('к. ', '')
    } else if (part.startsWith('кв.')) {
      result.apartment = part.replace('кв. ', '')
    }
  })

  return result
}

/**
 * Форматирование адреса из полей формы в строку
 */
const formatAddress = () => {
  const { city, street, house, building, apartment } = form.value
  let address = `г. ${city}, ул. ${street}, д. ${house}`
  if (building) address += `, к. ${building}`
  if (apartment) address += `, кв. ${apartment}`
  return address
}

/**
 * Обработчик отправки формы
 */
const handleSubmit = async () => {
  if (!validateForm()) return

  loading.value = true
  error.value = null

  try {
    const requestData: RequestCreateData = {
      client_name: form.value.client_name,
      phone: form.value.phone,
      address: formatAddress(),
      city: form.value.city,
      city_id: locationsStore.cities.find(c => c.name === form.value.city)?.id || 0,
      street: form.value.street,
      house: form.value.house,
      building: form.value.building,
      apartment: form.value.apartment,
      comment: form.value.comment,
      priority: form.value.priority
    }

    if (editMode.value && props.initialData) {
      await requestsStore.updateRequest(props.initialData.id, requestData)
    } else {
      await requestsStore.createRequest(requestData)
    }

    emit('success')
    if (!editMode.value) resetForm()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Произошла ошибка'
  } finally {
    loading.value = false
  }
}

// Инициализация компонента
onMounted(() => {
  locationsStore.fetchCities()
  if (props.initialData) {
    initForm()
  }
})
</script>

<style scoped>
.request-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
  background: var(--color-background-soft);
  border-radius: 8px;
}

.section-title {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  color: var(--color-text);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.address-row {
  display: flex;
  gap: 16px;
  grid-column: 1 / -1;
}

.address-input {
  flex: 1;
  min-width: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.form-error {
  margin-bottom: 16px;
}
</style>
