import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios'

// Базовый URL API из переменных окружения
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api'

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
    // Здесь можно добавить токен авторизации в будущем
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
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
  (error: AxiosError) => {
    // Обработка различных типов ошибок
    if (error.response) {
      // Сервер ответил с кодом ошибки
      const status = error.response.status
      const message = error.response.data?.message || error.message

      switch (status) {
        case 401:
          console.error('Не авторизован')
          // Здесь можно перенаправить на страницу входа
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
    const axiosError = error as AxiosError
    return {
      message: axiosError.response?.data?.detail || axiosError.message || 'Произошла ошибка',
      status: axiosError.response?.status,
      detail: axiosError.response?.data?.detail,
    }
  }
  return {
    message: error instanceof Error ? error.message : 'Неизвестная ошибка',
  }
}

export default apiClient

