import apiClient, { handleApiError } from './api'
import type { Achievement } from '@/types'

// Типы для API ответов
export interface AchievementResponse extends Achievement {
  unlocked_at?: string | null
}

export interface AchievementUnlockResponse {
  message: string
  achievement_id: string
  unlocked_at: string
}

/**
 * Получить список всех достижений с информацией о разблокировке
 */
export const getAchievements = async (): Promise<AchievementResponse[]> => {
  try {
    const response = await apiClient.get<AchievementResponse[]>('/achievements')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

/**
 * Разблокировать достижение (обычно вызывается автоматически)
 * @param achievementId - ID достижения
 */
export const unlockAchievement = async (achievementId: string): Promise<AchievementUnlockResponse> => {
  try {
    const response = await apiClient.post<AchievementUnlockResponse>(`/achievements/${achievementId}/unlock`)
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

