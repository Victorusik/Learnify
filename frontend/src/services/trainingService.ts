import apiClient, { handleApiError } from './api'
import type { Block } from '@/types'

export interface TrainingCardResponse {
  cards: Block[]
}

export interface TrainingSubmitRequest {
  block_id: string
  lesson_id: string
  course_id: string
  is_correct: boolean
}

export interface TrainingSubmitResponse {
  message: string
  next_review: string
  interval: number
  needs_review: boolean
}

export const getTrainingCards = async (): Promise<TrainingCardResponse> => {
  try {
    const response = await apiClient.get<TrainingCardResponse>('/training/cards')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

export const submitTrainingAnswer = async (data: TrainingSubmitRequest): Promise<TrainingSubmitResponse> => {
  try {
    const response = await apiClient.post<TrainingSubmitResponse>('/training/submit', data)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

