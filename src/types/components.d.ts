import { DefineComponent } from 'vue'

declare module 'vue' {
  export interface GlobalComponents {
    AppInput: DefineComponent<{
      modelValue: string
      label?: string
      type?: 'text' | 'password' | 'email' | 'number'
      error?: string
      disabled?: boolean
      placeholder?: string
    }>
    AppButton: DefineComponent<{
      type?: 'primary' | 'secondary' | 'danger'
      size?: 'small' | 'medium' | 'large'
      loading?: boolean
      disabled?: boolean
    }>
    AppModal: DefineComponent<{
      show: boolean
      title?: string
      size?: 'sm' | 'md' | 'lg'
    }>
    StatusBadge: DefineComponent<{
      status: 'unassigned' | 'assigned' | 'in_progress' | 'completed' | 'rejected'
    }>
    AppTable: DefineComponent<{
      headers: Array<{ text: string; value: string }>
      items: Array<Record<string, unknown>>
    }>
  }
}
