<template>
  <div class="user-edit">
    <h2>Редактирование пользователя</h2>
    <UserForm
      :initial-data="userData"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserForm from '@/components/features/Admin/UserForm.vue'
import { useUsersStore } from '@/stores/users.store'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const userData = ref<any>(null)

onMounted(async () => {
  userData.value = await usersStore.fetchUserById(route.params.id as string)
})

const handleSubmit = async (updatedData: any) => {
  await usersStore.updateUser(route.params.id as string, updatedData)
  router.push({ name: 'user-management' })
}
</script>
