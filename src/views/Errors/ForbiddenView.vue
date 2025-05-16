<template>
  <div class="forbidden-view">
    <h1>403 - Доступ запрещён</h1>
    <p>У вас недостаточно прав для просмотра этой страницы</p>
    <AppButton @click="goBack">Вернуться назад</AppButton>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppButton from '@/components/ui/AppButton.vue'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.forbidden-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}
</style>
