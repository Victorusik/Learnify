import axios, { type AxiosInstance, AxiosError, type AxiosResponse, type AxiosRequestConfig } from 'axios'
import { withRetry, type RetryOptions } from '@/utils/retry'
import { CircuitBreaker } from '@/utils/circuitBreaker'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api'

const circuitBreakers = {
  default: new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 }),
  read: new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 }),
  write: new CircuitBreaker({ failureThreshold: 3, resetTimeout: 60000 })
}

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError<{ message?: string; detail?: string }>) => {
    if (error.response) {
      const status = error.response.status
      const errorData = error.response.data
      const message = errorData?.message || errorData?.detail || error.message

      switch (status) {
        case 401:
          console.error('Не авторизован')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          }
          break
        case 403:
          console.error('Доступ запрещен')
          break
        case 404:
          console.error('Ресурс не найден')
          break
        case 500:
          console.error('Ошибка сервера')
          break
        default:
          console.error(`Ошибка ${status}: ${message}`)
      }
    } else if (error.request) {
      console.error('Нет ответа от сервера. Проверьте подключение к интернету.')
    } else {
      console.error('Ошибка при настройке запроса:', error.message)
    }

    return Promise.reject(error)
  }
)

export interface ApiError {
  message: string
  status?: number
  detail?: string
}

export const handleApiError = (error: unknown): ApiError => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string; message?: string }>
    const errorData = axiosError.response?.data
    return {
      message: errorData?.detail || errorData?.message || axiosError.message || 'Произошла ошибка',
      status: axiosError.response?.status,
      detail: errorData?.detail,
    }
  }
  return {
    message: error instanceof Error ? error.message : 'Неизвестная ошибка',
  }
}

async function resilientRequest<T>(
  requestFn: () => Promise<AxiosResponse<T>>,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    retryOptions?: RetryOptions
    circuitBreaker?: CircuitBreaker
  } = {}
): Promise<AxiosResponse<T>> {
  const { method = 'GET', retryOptions, circuitBreaker } = options

  const breaker = circuitBreaker ||
    (method === 'GET' ? circuitBreakers.read : circuitBreakers.write) ||
    circuitBreakers.default

  const executeWithBreaker = () => breaker.execute(() => requestFn())

  return withRetry(executeWithBreaker, {
    maxRetries: 3,
    initialDelay: 1000,
    maxDelay: 10000,
    ...retryOptions
  })
}

export async function resilientGet<T>(
  url: string,
  config?: AxiosRequestConfig,
  retryOptions?: RetryOptions
): Promise<AxiosResponse<T>> {
  return resilientRequest(
    () => apiClient.get<T>(url, config),
    { method: 'GET', retryOptions }
  )
}

export async function resilientPost<T>(
  url: string,
  data?: any,
  config?: AxiosRequestConfig,
  retryOptions?: RetryOptions
): Promise<AxiosResponse<T>> {
  return resilientRequest(
    () => apiClient.post<T>(url, data, config),
    { method: 'POST', retryOptions }
  )
}

export async function resilientPut<T>(
  url: string,
  data?: any,
  config?: AxiosRequestConfig,
  retryOptions?: RetryOptions
): Promise<AxiosResponse<T>> {
  return resilientRequest(
    () => apiClient.put<T>(url, data, config),
    { method: 'PUT', retryOptions }
  )
}

export async function resilientDelete<T>(
  url: string,
  config?: AxiosRequestConfig,
  retryOptions?: RetryOptions
): Promise<AxiosResponse<T>> {
  return resilientRequest(
    () => apiClient.delete<T>(url, config),
    { method: 'DELETE', retryOptions }
  )
}

export default apiClient

