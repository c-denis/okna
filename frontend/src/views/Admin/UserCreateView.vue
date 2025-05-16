<template>
  <div class="user-create">
    <h2>Создание пользователя</h2>
    <UserForm @submit="handleSubmit" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import UserForm from '@/components/features/Admin/UserForm.vue'
import { useUsersStore } from '@/stores/users.store'

const router = useRouter()
const usersStore = useUsersStore()

const handleSubmit = async (userData: any) => {
  await usersStore.createUser(userData)
  router.push({ name: 'user-management' })
}
</script>

<style scoped>
.user-create {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
