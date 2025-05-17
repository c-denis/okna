<template>
  <AuthLayout>
    <div class="login-view">
      <LoginForm />
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from '@/layouts/AuthLayout.vue';
import LoginForm from '@/features/Auth/LoginForm.vue';
</script>

<style scoped>
.login-view {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
