import apiClient, { handleApiError } from './api'
import type { Achievement } from '@/types'

export interface AchievementResponse extends Achievement {
  unlocked_at?: string | null
}

export interface AchievementUnlockResponse {
  message: string
  achievement_id: string
  unlocked_at: string
}

export const getAchievements = async (): Promise<AchievementResponse[]> => {
  try {
    const response = await apiClient.get<AchievementResponse[]>('/achievements')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

export const unlockAchievement = async (achievementId: string): Promise<AchievementUnlockResponse> => {
  try {
    const response = await apiClient.post<AchievementUnlockResponse>(`/achievements/${achievementId}/unlock`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

