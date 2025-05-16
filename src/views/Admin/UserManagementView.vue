<template>
  <div class="user-management">
    <div class="header">
      <h1>Управление пользователями</h1>
      <RouterLink
        :to="{ name: 'user-create' }"
        class="create-btn"
      >
        Создать пользователя
      </RouterLink>
    </div>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.user-management {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.create-btn {
  background: #3498db;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
}
</style>
