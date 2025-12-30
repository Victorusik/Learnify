import { resilientGet, resilientPost, handleApiError } from './api'
import { cache } from '@/utils/cache'
import type { Course } from '@/types'

// Типы для API ответов
// Используем Omit чтобы исключить поле category из базового типа Course,
// так как API возвращает category как объект, а не строку
export interface CourseResponse extends Omit<Course, 'category'> {
  category?: {
    id: string
    name: string
    icon: string
  }
  creation_date?: string
  last_updated?: string
}

export interface CourseEnrollResponse {
  message: string
  course_id: string
}

export interface LessonListItem {
  id: string
  order: number
  title: string
  description: string
}

/**
 * Получить список всех курсов с кэшированием и fallback
 * @param categoryId - опциональный фильтр по категории
 */
export const getCourses = async (categoryId?: string): Promise<CourseResponse[]> => {
  const cacheKey = `courses_${categoryId || 'all'}`

  try {
    const params = categoryId ? { category_id: categoryId } : {}
    const response = await resilientGet<CourseResponse[]>('/courses', { params })

    // Сохраняем в кэш на 5 минут
    cache.set(cacheKey, response.data, 300000)

    return response.data
  } catch (error) {
    // Пытаемся получить из кэша при ошибке
    const cached = cache.get<CourseResponse[]>(cacheKey)
    if (cached) {
      console.warn('Using cached data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

/**
 * Получить детали курса по ID с кэшированием
 * @param courseId - ID курса
 */
export const getCourse = async (courseId: string): Promise<CourseResponse> => {
  const cacheKey = `course_${courseId}`

  try {
    const response = await resilientGet<CourseResponse>(`/courses/${courseId}`)

    // Сохраняем в кэш на 10 минут
    cache.set(cacheKey, response.data, 600000)

    return response.data
  } catch (error) {
    // Пытаемся получить из кэша
    const cached = cache.get<CourseResponse>(cacheKey)
    if (cached) {
      console.warn('Using cached course data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

/**
 * Записаться на курс (без кэширования, так как это операция записи)
 * @param courseId - ID курса
 */
export const enrollCourse = async (courseId: string): Promise<CourseEnrollResponse> => {
  try {
    const response = await resilientPost<CourseEnrollResponse>(
      `/courses/${courseId}/enroll`,
      {},
      {},
      { maxRetries: 2 } // Меньше попыток для операций записи
    )
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Получить список уроков курса с кэшированием
 * @param courseId - ID курса
 */
export const getCourseLessons = async (courseId: string): Promise<LessonListItem[]> => {
  const cacheKey = `lessons_${courseId}`

  try {
    const response = await resilientGet<LessonListItem[]>(`/courses/${courseId}/lessons`)

    // Сохраняем в кэш на 5 минут
    cache.set(cacheKey, response.data, 300000)

    return response.data
  } catch (error) {
    // Пытаемся получить из кэша
    const cached = cache.get<LessonListItem[]>(cacheKey)
    if (cached) {
      console.warn('Using cached lessons data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

