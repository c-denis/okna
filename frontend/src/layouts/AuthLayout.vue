<template>
  <div class="auth-layout">
    <div class="logo">
      <img src="@/assets/logo.svg" alt="CRM Okna">
    </div>
    <div class="form-container">
      <router-view />
    </div>
    <footer class="footer">
      <router-link to="/forgot-password">Забыли пароль?</router-link>
      <span>|</span>
      <router-link to="/register">Регистрация</router-link>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.auth-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #3498db, #2c3e50);
}

.logo {
  margin-bottom: 40px;
}

.logo img {
  height: 60px;
}

.form-container {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.footer {
  margin-top: 20px;
  color: white;
  display: flex;
  gap: 12px;
}

.footer a {
  color: white;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}
</style>
