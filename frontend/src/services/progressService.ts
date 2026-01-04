import apiClient, { handleApiError } from './api'

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

export const getProgress = async (): Promise<UserProgressResponse> => {
  try {
    const response = await apiClient.get<UserProgressResponse>('/progress')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

export const markBlockCompleted = async (data: BlockProgressCreate): Promise<ProgressResponse> => {
  try {
    const response = await apiClient.post<ProgressResponse>('/progress/block', data)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

export const markLessonCompleted = async (data: LessonProgressCreate): Promise<ProgressResponse> => {
  try {
    const response = await apiClient.post<ProgressResponse>('/progress/lesson', data)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

