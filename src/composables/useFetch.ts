import { ref } from 'vue'
import axios, { type AxiosResponse, type AxiosError } from '@/api/client'

export function useFetch<T>() {
  const data = ref<T>()
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchData = async (url: string, params?: Record<string, unknown>) => {
    loading.value = true
    error.value = null
    try {
      const response: AxiosResponse<T> = await axios.get(url, { params })
      data.value = response.data
    } catch (err) {
      const axiosError = err as AxiosError
      error.value = axiosError.message || 'An error occurred'
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}
