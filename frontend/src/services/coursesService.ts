import apiClient, { handleApiError } from './api'
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
 * Получить список всех курсов
 * @param categoryId - опциональный фильтр по категории
 */
export const getCourses = async (categoryId?: string): Promise<CourseResponse[]> => {
  try {
    const params = categoryId ? { category_id: categoryId } : {}
    const response = await apiClient.get<CourseResponse[]>('/courses', { params })
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Получить детали курса по ID
 * @param courseId - ID курса
 */
export const getCourse = async (courseId: string): Promise<CourseResponse> => {
  try {
    const response = await apiClient.get<CourseResponse>(`/courses/${courseId}`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Записаться на курс
 * @param courseId - ID курса
 */
export const enrollCourse = async (courseId: string): Promise<CourseEnrollResponse> => {
  try {
    const response = await apiClient.post<CourseEnrollResponse>(`/courses/${courseId}/enroll`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Получить список уроков курса
 * @param courseId - ID курса
 */
export const getCourseLessons = async (courseId: string): Promise<LessonListItem[]> => {
  try {
    const response = await apiClient.get<LessonListItem[]>(`/courses/${courseId}/lessons`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

