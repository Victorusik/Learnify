import apiClient, { handleApiError } from './api'
import type { Lesson } from '@/types'

/**
 * Получить детали урока с блоками
 * @param lessonId - ID урока
 */
export const getLesson = async (lessonId: string): Promise<Lesson> => {
  try {
    const response = await apiClient.get<Lesson>(`/lessons/${lessonId}`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

