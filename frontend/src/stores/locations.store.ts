import { defineStore } from 'pinia'
import httpClient from '@/utils/httpClient'
import type { AxiosResponse } from 'axios'

/**
 * Интерфейс для описания города
 */
interface City {
  id: number          // Уникальный идентификатор города
  name: string        // Название города
  region?: string     // Регион (опционально)
  country?: string    // Страна (опционально)
}

/**
 * Интерфейс для описания улицы
 */
interface Street {
  id: number          // Уникальный идентификатор улицы
  name: string        // Название улицы
  city_id: number     // ID города, к которому относится улица
  postal_code?: string // Почтовый индекс (опционально)
}

/**
 * Состояние хранилища локаций
 */
interface LocationsState {
  cities: City[]              // Список городов
  streets: Street[]           // Список улиц (для выбранного города)
  loading: boolean            // Флаг загрузки данных
  error: string | null        // Последняя ошибка
  lastUpdated: number | null  // Время последнего обновления (timestamp)
}

/**
 * Хранилище для работы с географическими локациями
 *
 * Используется в:
 * - Формах создания/редактирования заявок
 * - Фильтрах списка заявок
 * - Любых местах, где требуется выбор города/улицы
 */
export const useLocationsStore = defineStore('locations', {
  state: (): LocationsState => ({
    cities: [],
    streets: [],
    loading: false,
    error: null,
    lastUpdated: null
  }),

  actions: {
    /**
     * Загружает список городов с сервера
     * @param force - Принудительная загрузка, даже если данные уже есть
     */
    async fetchCities(force: boolean = false): Promise<void> {
      // Если города уже загружены и не требуется принудительная загрузка
      if (this.cities.length > 0 && !force) return

      this.loading = true
      this.error = null

      try {
        const response: AxiosResponse<City[]> = await httpClient.get('/api/v1/cities')
        this.cities = response.data
        this.lastUpdated = Date.now()
      } catch (error) {
        console.error('Ошибка загрузки городов:', error)
        this.error = 'Не удалось загрузить список городов'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Загружает список улиц для указанного города
     * @param cityName - Название города
     * @param force - Принудительная загрузка, даже если данные уже есть
     */
    async fetchStreets(cityName: string, force: boolean = false): Promise<void> {
      // Находим город по имени
      const city = this.cities.find(c => c.name === cityName)
      if (!city) {
        this.error = 'Город не найден'
        return
      }

      // Если улицы уже загружены для этого города и не требуется принудительная загрузка
      if (this.streets.length > 0 && this.streets[0].city_id === city.id && !force) return

      this.loading = true
      this.error = null

      try {
        const response: AxiosResponse<Street[]> = await httpClient.get(
          `/api/v1/cities/${city.id}/streets`
        )
        this.streets = response.data
      } catch (error) {
        console.error('Ошибка загрузки улиц:', error)
        this.error = 'Не удалось загрузить список улиц'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Сбрасывает список улиц (например, при смене города)
     */
    resetStreets(): void {
      this.streets = []
    },

    /**
     * Сбрасывает все ошибки хранилища
     */
    clearErrors(): void {
      this.error = null
    }
  },

  getters: {
    /**
     * Возвращает список городов в формате для выпадающего списка
     * Формат: { value: string, label: string }
     */
    cityOptions(state): Array<{ value: string; label: string }> {
      return state.cities.map(city => ({
        value: city.name,
        label: city.name
      }))
    },

    /**
     * Возвращает список улиц в формате для выпадающего списка
     * Формат: { value: string, label: string }
     */
    streetOptions(state): Array<{ value: string; label: string }> {
      return state.streets.map(street => ({
        value: street.name,
        label: street.name
      }))
    },

    /**
     * Проверяет, загружены ли города
     */
    hasCities(state): boolean {
      return state.cities.length > 0
    },

    /**
     * Проверяет, загружены ли улицы
     */
    hasStreets(state): boolean {
      return state.streets.length > 0
    },

    /**
     * Возвращает город по ID
     */
    getCityById: (state) => (id: number): City | undefined => {
      return state.cities.find(city => city.id === id)
    },

    /**
     * Возвращает улицу по ID
     */
    getStreetById: (state) => (id: number): Street | undefined => {
      return state.streets.find(street => street.id === id)
    }
  }
})

/**
 * Типы для экспорта
 */
export type { City, Street }
