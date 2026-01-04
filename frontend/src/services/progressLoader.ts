import { getProgress } from './progressService'
import type { UserProgressResponse } from './progressService'

export const loadUserProgress = async (): Promise<UserProgressResponse> => {
  try {
    const progress = await getProgress()
    return progress
  } catch (error) {
    console.error('Failed to load user progress:', error)
    throw error
  }
}

export const parseProgressForStores = (progress: UserProgressResponse) => {
  const lessonsProgress = new Map<string, number>()
  const completedLessons = new Set<string>()

  const lessonBlocksCount = new Map<string, { completed: number; total: number }>()

  progress.progress.forEach(item => {
    const current = lessonsProgress.get(item.lesson_id) || 0
    lessonsProgress.set(item.lesson_id, current + 1)

    if (!lessonBlocksCount.has(item.lesson_id)) {
      lessonBlocksCount.set(item.lesson_id, { completed: 0, total: 0 })
    }
    const lessonData = lessonBlocksCount.get(item.lesson_id)!
    lessonData.completed += 1
  })

  return {
    lessonsProgress,
    completedLessons: Array.from(completedLessons),
    totalBlocksCompleted: progress.total_blocks_completed
  }
}

