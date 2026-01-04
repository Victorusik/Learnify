import { resilientGet, resilientPost, handleApiError } from './api'
import { cache } from '@/utils/cache'
import type { Course } from '@/types'

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

export const getCourses = async (categoryId?: string): Promise<CourseResponse[]> => {
  const cacheKey = `courses_${categoryId || 'all'}`

  try {
    const params = categoryId ? { category_id: categoryId } : {}
    const response = await resilientGet<CourseResponse[]>('/courses', { params })

    cache.set(cacheKey, response.data, 300000)

    return response.data
  } catch (error) {
    const cached = cache.get<CourseResponse[]>(cacheKey)
    if (cached) {
      console.warn('Using cached data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

export const getCourse = async (courseId: string): Promise<CourseResponse> => {
  const cacheKey = `course_${courseId}`

  try {
    const response = await resilientGet<CourseResponse>(`/courses/${courseId}`)

    cache.set(cacheKey, response.data, 600000)

    return response.data
  } catch (error) {
    const cached = cache.get<CourseResponse>(cacheKey)
    if (cached) {
      console.warn('Using cached course data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

export const enrollCourse = async (courseId: string): Promise<CourseEnrollResponse> => {
  try {
    const response = await resilientPost<CourseEnrollResponse>(
      `/courses/${courseId}/enroll`,
      {},
      {},
      { maxRetries: 2 }
    )
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

export const getCourseLessons = async (courseId: string): Promise<LessonListItem[]> => {
  const cacheKey = `lessons_${courseId}`

  try {
    const response = await resilientGet<LessonListItem[]>(`/courses/${courseId}/lessons`)

    cache.set(cacheKey, response.data, 300000)

    return response.data
  } catch (error) {
    const cached = cache.get<LessonListItem[]>(cacheKey)
    if (cached) {
      console.warn('Using cached lessons data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

