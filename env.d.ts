/// <reference types="vite/client" />
/// <reference types="unplugin-icons/types/vue" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_URL: string
  // Другие переменные окружения...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}