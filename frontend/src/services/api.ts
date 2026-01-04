import axios, { type AxiosInstance, AxiosError, type AxiosResponse, type AxiosRequestConfig } from 'axios'
import { withRetry, type RetryOptions } from '@/utils/retry'
import { CircuitBreaker } from '@/utils/circuitBreaker'

// Базовый URL API из переменных окружения
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api'

// Circuit breakers для разных типов запросов
const circuitBreakers = {
  default: new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 }),
  read: new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 }),
  write: new CircuitBreaker({ failureThreshold: 3, resetTimeout: 60000 })
}

// Создание экземпляра axios с базовой конфигурацией
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 секунд
  headers: {
    'Content-Type': 'application/json',
  },
})

// Интерцептор для обработки запросов
apiClient.interceptors.request.use(
  (config) => {
    // Добавляем токен авторизации в заголовки
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

// Интерцептор для обработки ответов
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError<{ message?: string; detail?: string }>) => {
    // Обработка различных типов ошибок
    if (error.response) {
      // Сервер ответил с кодом ошибки
      const status = error.response.status
      const errorData = error.response.data
      const message = errorData?.message || errorData?.detail || error.message

      switch (status) {
        case 401:
          console.error('Не авторизован')
          // Очищаем токены
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          // Редирект на логин, если мы не на странице логина/регистрации
          // Используем router вместо window.location для правильной навигации
          if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
            // Не делаем редирект здесь, пусть router guard обработает это
            // Просто очищаем токены, router guard перенаправит
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
      // Запрос был отправлен, но ответа не получено
      console.error('Нет ответа от сервера. Проверьте подключение к интернету.')
    } else {
      // Ошибка при настройке запроса
      console.error('Ошибка при настройке запроса:', error.message)
    }

    return Promise.reject(error)
  }
)

// Типы для API ответов
export interface ApiError {
  message: string
  status?: number
  detail?: string
}

// Вспомогательная функция для обработки ошибок
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

/**
 * Выполняет запрос с retry и circuit breaker
 */
async function resilientRequest<T>(
  requestFn: () => Promise<AxiosResponse<T>>,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    retryOptions?: RetryOptions
    circuitBreaker?: CircuitBreaker
  } = {}
): Promise<AxiosResponse<T>> {
  const { method = 'GET', retryOptions, circuitBreaker } = options

  // Выбираем circuit breaker в зависимости от типа запроса
  const breaker = circuitBreaker ||
    (method === 'GET' ? circuitBreakers.read : circuitBreakers.write) ||
    circuitBreakers.default

  // Выполняем через circuit breaker
  const executeWithBreaker = () => breaker.execute(() => requestFn())

  // Добавляем retry с exponential backoff
  return withRetry(executeWithBreaker, {
    maxRetries: 3,
    initialDelay: 1000,
    maxDelay: 10000,
    ...retryOptions
  })
}

/**
 * Обертка для GET запросов с отказоустойчивостью
 */
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

/**
 * Обертка для POST запросов с отказоустойчивостью
 */
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

/**
 * Обертка для PUT запросов с отказоустойчивостью
 */
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

/**
 * Обертка для DELETE запросов с отказоустойчивостью
 */
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

