<template>
  <component :is="currentComponent" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import LoginForm from '@/components/features/Auth/LoginForm.vue'
import RegisterForm from '@/components/features/Auth/RegisterForm.vue'
import ForgotPasswordForm from '@/components/features/Auth/ForgotPasswordForm.vue'

const route = useRoute()

const currentComponent = computed(() => {
  switch (route.name) {
    case 'login':
      return LoginForm
    case 'register':
      return RegisterForm
    case 'forgot-password':
      return ForgotPasswordForm
    default:
      return LoginForm
  }
})
</script>

<style scoped>
.auth-view {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
