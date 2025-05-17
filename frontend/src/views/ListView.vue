<template>
  <MainLayout>
    <div class="requests-list-view">
      <h1>Список заявок</h1>

      <!-- Компонент списка из features -->
      <RequestList />

      <!-- Кнопка создания новой заявки -->
      <AppButton
        @click="openCreateModal"
        class="create-button"
      >
        Создать заявку
      </AppButton>

      <!-- Модальное окно создания -->
      <RequestFormModal
        v-if="showCreateModal"
        @close="showCreateModal = false"
      />
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue';
import RequestList from '@/features/Requests/RequestList.vue';
import RequestFormModal from '@/features/Requests/RequestForm.vue';
import AppButton from '@/components/ui/AppButton.vue';
import { ref } from 'vue';

const showCreateModal = ref(false);

const openCreateModal = () => {
  showCreateModal.value = true;
};
</script>

<style scoped>
.requests-list-view {
  padding: 24px;
}

.create-button {
  margin-top: 20px;
}
</style>
