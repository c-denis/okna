<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Страница не найдена</p>
    <AppButton @click="goHome">На главную</AppButton>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppButton from '@/components/ui/AppButton.vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

.not-found h1 {
  font-size: 5rem;
  margin-bottom: 1rem;
  color: var(--color-danger);
}

.not-found p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}
</style>
