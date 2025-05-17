<template>
  <MainLayout>
    <div class="settings-view">
      <h1 class="settings-view__title">Настройки</h1>

      <div class="settings-view__sections">
        <!-- Профиль -->
        <section class="settings-section">
          <h2 class="settings-section__title">
            <UsersIcon class="icon" />
            Профиль
          </h2>
          <AppInput
            v-model="user.name"
            label="Имя"
            placeholder="Введите ваше имя"
          />
          <AppInput
            v-model="user.email"
            label="Email"
            type="email"
            placeholder="example@mail.com"
          />
        </section>

        <!-- Безопасность -->
        <section class="settings-section">
          <h2 class="settings-section__title">
            <LogoutIcon class="icon" />
            Безопасность
          </h2>
          <AppInput
            v-model="password.current"
            label="Текущий пароль"
            type="password"
          />
          <AppInput
            v-model="password.new"
            label="Новый пароль"
            type="password"
          />
        </section>

        <!-- Действия -->
        <div class="settings-view__actions">
          <AppButton variant="outlined">Отменить</AppButton>
          <AppButton @click="saveSettings">Сохранить</AppButton>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue';
import AppInput from '@/components/ui/AppInput.vue';
import AppButton from '@/components/ui/AppButton.vue';
import UsersIcon from '@/components/icons/UsersIcon.vue';
import LogoutIcon from '@/components/icons/LogoutIcon.vue';
import { ref } from 'vue';

// Типы и логика
interface UserSettings {
  name: string;
  email: string;
}

interface PasswordSettings {
  current: string;
  new: string;
}

const user = ref<UserSettings>({
  name: '',
  email: '',
});

const password = ref<PasswordSettings>({
  current: '',
  new: '',
});

const saveSettings = () => {
  console.log('Сохранение настроек:', {
    user: user.value,
    password: password.value
  });
  // Здесь будет вызов API для сохранения
};
</script>

<style scoped>
.settings-view {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;

  &__title {
    font-size: 24px;
    margin-bottom: 32px;
    color: var(--text-primary);
  }

  &__sections {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  &__actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
  }
}

.settings-section {
  background: var(--bg-card);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

  &__title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    margin-bottom: 16px;
    color: var(--text-primary);

    .icon {
      width: 20px;
      height: 20px;
      color: var(--primary);
    }
  }
}
</style>
