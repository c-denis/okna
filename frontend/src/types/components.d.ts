import { DefineComponent } from 'vue'

/**
 * Декларация глобальных компонентов для TypeScript
 * Расширяет стандартные типы Vue для поддержки автодополнения
 * и проверки пропсов в IDE
 */
declare module 'vue' {
  export interface GlobalComponents {
    /**
     * Компонент текстового поля ввода
     * @props modelValue - Значение поля (обязательное)
     * @props label - Подпись поля (опционально)
     * @props type - Тип поля (по умолчанию 'text')
     * @props error - Текст ошибки (опционально)
     * @props disabled - Флаг disabled (опционально)
     * @props placeholder - Плейсхолдер (опционально)
     */
    AppInput: DefineComponent<{
      modelValue: string
      label?: string
      type?: 'text' | 'password' | 'email' | 'number'
      error?: string
      disabled?: boolean
      placeholder?: string
    }>

    /**
     * Компонент кнопки
     * @props variant - Вариант стиля кнопки
     * @props size - Размер кнопки
     * @props loading - Флаг состояния загрузки
     * @props disabled - Флаг disabled
     */
    AppButton: DefineComponent<{
      variant?: 'primary' | 'secondary' | 'outlined' | 'text' | 'danger'
      size?: 'small' | 'medium' | 'large'
      loading?: boolean
      disabled?: boolean
    }>

    /**
     * Компонент модального окна
     * @props show - Флаг видимости (обязательный)
     * @props title - Заголовок окна (опционально)
     * @props size - Размер окна (sm/md/lg)
     */
    AppModal: DefineComponent<{
      show: boolean
      title?: string
      size?: 'sm' | 'md' | 'lg'
    }>

    /**
     * Компонент бейджа статуса
     * @props status - Статус заявки (обязательный)
     */
    StatusBadge: DefineComponent<{
      status: 'unassigned' | 'assigned' | 'in_progress' | 'completed' | 'rejected'
    }>

    /**
     * Компонент таблицы данных
     * @props headers - Заголовки колонок (обязательный)
     * @props items - Данные для отображения (обязательный)
     * @props emptyMessage - Сообщение при пустой таблице (опционально)
     */
    AppTable: DefineComponent<{
      headers: Array<{
        text: string
        value: string
        width?: string
        align?: 'left' | 'center' | 'right'
      }>
      items: Array<Record<string, unknown>>
      emptyMessage?: string
    }>

    /**
     * Компонент селекта
     * @props modelValue - Выбранное значение (обязательное)
     * @props options - Варианты выбора (обязательные)
     * @props placeholder - Плейсхолдер (опционально)
     * @props clearable - Флаг возможности очистки (опционально)
     */
    AppSelect: DefineComponent<{
      modelValue: any
      options: Array<{
        value: any
        label: string
        disabled?: boolean
      }>
      placeholder?: string
      clearable?: boolean
    }>

    /**
     * Компонент иконки
     * @props name - Название иконки (обязательное)
     * @props size - Размер иконки (опционально)
     * @props color - Цвет иконки (опционально)
     */
    AppIcon: DefineComponent<{
      name: string
      size?: 'small' | 'medium' | 'large'
      color?: 'primary' | 'secondary' | 'error' | 'success' | 'warning'
    }>

    /**
     * Компонент спиннера загрузки
     * @props size - Размер спиннера (опционально)
     */
    AppSpinner: DefineComponent<{
      size?: 'small' | 'medium' | 'large'
    }>

    /**
     * Компонент алерта
     * @props type - Тип алерта (обязательный)
     * @props message - Текст сообщения (обязательный)
     */
    AppAlert: DefineComponent<{
      type: 'success' | 'error' | 'warning' | 'info'
      message: string
    }>

    /**
     * Модальное окно назначения заявки
     * @props request - Данные заявки (обязательные)
     * @props managers - Список доступных менеджеров (обязательные)
     * @emits close - Событие закрытия окна
     * @emits assign - Событие назначения менеджера
     */
    AssignModal: DefineComponent<{
      request: {
        id: string
        status: string
        assigned_to?: {
          id: string
          name: string
        }
      }
      managers: Array<{
        id: string
        name: string
        status: string
      }>
    }>

    /**
     * Модальное окно деталей заявки
     * @props request - Данные заявки (обязательные)
     * @emits close - Событие закрытия окна
     * @emits status-update - Событие обновления статуса
     * @emits blacklist - Событие добавления в ЧС
     */
    RequestDetailsModal: DefineComponent<{
      request: {
        id: string
        client_name: string
        phone: string
        address: string
        status: string
        created_at: string
        is_blacklisted: boolean
      }
    }>
  }
}
