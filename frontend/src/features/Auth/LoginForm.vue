<template>
  <form @submit.prevent="handleSubmit" class="login-form">
    <AppInput
      v-model="form.email"
      type="email"
      label="Email"
      placeholder="Введите ваш email"
      required
    />

    <AppInput
      v-model="form.password"
      type="password"
      label="Пароль"
      placeholder="Введите пароль"
      required
    />

    <div class="form-actions">
      <AppButton
        type="submit"
        :loading="loading"
        :disabled="loading"
      >
        Войти
      </AppButton>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore();

const form = ref({
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  try {
    loading.value = true;
    error.value = '';
    await authStore.login(form.value.email, form.value.password);
  } catch (err) {
    error.value = 'Неверный email или пароль';
    console.error('Login error:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.form-actions {
  margin-top: 24px;
  text-align: center;
}

.error-message {
  margin-top: 16px;
  color: #d32f2f;
  text-align: center;
  font-size: 0.9rem;
}
</style>
