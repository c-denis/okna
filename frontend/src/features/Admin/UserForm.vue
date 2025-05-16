<template>
  <form class="user-form" @submit.prevent="handleSubmit">
    <AppInput
      v-model="form.name"
      label="Имя"
      required
    />
    <AppInput
      v-model="form.email"
      label="Email"
      type="email"
      required
    />
    <AppSelect
      v-model="form.role"
      label="Роль"
      :options="roleOptions"
      required
    />
    <AppButton type="submit">
      Сохранить
    </AppButton>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppButton from '@/components/ui/AppButton.vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit'])

const form = ref({
  name: '',
  email: '',
  role: 'operator'
})

watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = { ...newVal }
  }
}, { immediate: true })

const roleOptions = [
  { value: 'admin', text: 'Администратор' },
  { value: 'coordinator', text: 'Координатор' },
  { value: 'manager', text: 'Менеджер' },
  { value: 'operator', text: 'Оператор' }
]

const handleSubmit = () => {
  emit('submit', form.value)
}
</script>

<style scoped>
.user-form {
  display: grid;
  gap: 16px;
  max-width: 500px;
}
</style>
