import { resilientGet, handleApiError } from './api'
import { cache } from '@/utils/cache'
import type { Lesson } from '@/types'

export const getLesson = async (lessonId: string): Promise<Lesson> => {
  const cacheKey = `lesson_${lessonId}`

  try {
    const response = await resilientGet<Lesson>(`/lessons/${lessonId}`)

    cache.set(cacheKey, response.data, 600000)

    return response.data
  } catch (error) {
    const cached = cache.get<Lesson>(cacheKey)
    if (cached) {
      console.warn('Using cached lesson data due to API error')
      return cached
    }
    throw handleApiError(error)
  }
}

