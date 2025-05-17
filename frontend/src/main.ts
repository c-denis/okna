import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import registerComponents from '@/utils/register-components'
import useAuthStore from '@/stores/auth.store'

import '@/assets/styles/main.css'

const app = createApp(App)

// Плагины
app.use(createPinia())
app.use(router)

// Глобальные компоненты
registerComponents(app)

// Проверка аутентификации при загрузке
const authStore = useAuthStore()
authStore.checkAuth().finally(() => {
  app.mount('#app')
})
