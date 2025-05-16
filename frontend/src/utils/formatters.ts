import { type Ref } from 'vue'
import type { Request } from '@/types/requests'

/**
 * Форматирование даты в читаемый формат
 * @param date Строка даты или объект Date
 * @returns Строка в формате "дд.мм.гггг чч:мм"
 */
export const formatDate = (date: string | Date): string => {
  const d = new Date(date)
  return d.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * Форматирование номера телефона
 * @param phone Номер телефона в любом формате
 * @returns Строка в формате "+7 (XXX) XXX-XX-XX"
 */
export const formatPhone = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '')
  const match = cleaned.match(/^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})$/)
  if (match) {
    return `+${match[1]} (${match[2]}) ${match[3]}-${match[4]}-${match[5]}`
  }
  return phone
}

/**
 * Форматирование статуса заявки
 * @param status Статус заявки
 * @returns Человеко-читаемый статус
 */
export const formatRequestStatus = (status: Request['status']): string => {
  const statusMap: Record<Request['status'], string> = {
    unassigned: 'Не назначена',
    assigned: 'Назначена',
    in_progress: 'В работе',
    completed: 'Выполнена',
    rejected: 'Отказ'
  }
  return statusMap[status] || status
}

/**
 * Форматирование ФИО
 * @param name Полное имя
 * @returns Сокращенное ФИО (И.О. Фамилия)
 */
export const formatShortName = (name: string): string => {
  const parts = name.split(' ')
  if (parts.length === 3) {
    return `${parts[1][0]}.${parts[2][0]}. ${parts[0]}`
  }
  return name
}
