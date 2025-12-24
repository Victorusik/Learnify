import apiClient, { handleApiError } from './api'

// Типы для API запросов и ответов
export interface BlockProgressCreate {
  block_id: string
  lesson_id: string
  course_id: string
}

export interface LessonProgressCreate {
  lesson_id: string
  course_id: string
}

export interface ProgressResponse {
  message: string
  block_id?: string
  lesson_id?: string
}

export interface ProgressItem {
  block_id: string
  lesson_id: string
  course_id: string
  completed_at: string | null
}

export interface UserProgressResponse {
  total_blocks_completed: number
  progress: ProgressItem[]
}

/**
 * Получить весь прогресс пользователя
 */
export const getProgress = async (): Promise<UserProgressResponse> => {
  try {
    const response = await apiClient.get<UserProgressResponse>('/progress')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Отметить блок как выполненный
 * @param data - данные о прогрессе блока
 */
export const markBlockCompleted = async (data: BlockProgressCreate): Promise<ProgressResponse> => {
  try {
    const response = await apiClient.post<ProgressResponse>('/progress/block', data)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Отметить урок как завершенный
 * @param data - данные о прогрессе урока
 */
export const markLessonCompleted = async (data: LessonProgressCreate): Promise<ProgressResponse> => {
  try {
    const response = await apiClient.post<ProgressResponse>('/progress/lesson', data)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

