import apiClient, { handleApiError } from './api'
import type { Category } from '@/types'

/**
 * Получить список всех категорий
 */
export const getCategories = async (): Promise<Category[]> => {
  try {
    const response = await apiClient.get<Category[]>('/categories')
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}




