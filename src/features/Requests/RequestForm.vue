<template>
  <form @submit.prevent="handleSubmit">
    <AppInput v-model="form.clientName" label="ФИО клиента" />
    <AppButton type="submit">Создать заявку</AppButton>
  </form>
</template>

<script setup lang="ts">
import { useRequestsStore } from '@/stores/requests.store';

const requestsStore = useRequestsStore();
const form = ref({
  clientName: '',
  phone: '',
});

const handleSubmit = () => {
  requestsStore.createRequest(form.value);
};
</script>
