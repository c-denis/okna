<template>
  <div class="settings-view">
    <h1>Настройки системы</h1>
    <div class="settings-form">
      <AppInput
        v-model="settings.title"
        label="Название CRM"
      />
      <AppButton @click="saveSettings">
        Сохранить
      </AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'

const settings = ref({
  title: 'CRM Okna'
})

const saveSettings = () => {
  console.log('Settings saved:', settings.value)
}
</script>

<style scoped>
.settings-view {
  padding: 20px;
}
.settings-form {
  max-width: 500px;
  margin-top: 20px;
}
</style>
