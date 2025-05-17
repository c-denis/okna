<template>
  <AuthLayout>
    <h1>Регистрация</h1>
    <!-- Добавьте форму регистрации -->
    <AppButton @click="register">
      Зарегистрироваться
    </AppButton>
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from '@/layouts/AuthLayout.vue'
import AppButton from '@/components/ui/AppButton.vue'

const register = () => {
  // Логика регистрации
}
</script>
