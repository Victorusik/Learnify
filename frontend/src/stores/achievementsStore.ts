import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Achievement, UserStatistics } from '@/types'

export const useAchievementsStore = defineStore('achievements', () => {
  const unlockedAchievements = ref<Achievement[]>([])
  const weeklyActivity = ref<{ day: string; lessons: number }[]>([
    { day: 'Пн', lessons: 8 },
    { day: 'Вт', lessons: 15 },
    { day: 'Ср', lessons: 10 },
    { day: 'Чт', lessons: 12 },
    { day: 'Пт', lessons: 7 },
    { day: 'Сб', lessons: 5 },
    { day: 'Вс', lessons: 3 }
  ])

  const statistics = ref<UserStatistics>({
    totalLessons: 156,
    averageAccuracy: 87,
    daysLearning: 45,
    totalCardsReviewed: 1245
  })

  const unlockAchievement = (achievement: Achievement) => {
    if (!unlockedAchievements.value.find(a => a.id === achievement.id)) {
      achievement.unlocked = true
      achievement.unlockedAt = new Date()
      unlockedAchievements.value.push(achievement)
    }
  }

  const updateWeeklyActivity = (day: string, lessons: number) => {
    const dayData = weeklyActivity.value.find(d => d.day === day)
    if (dayData) {
      dayData.lessons = lessons
    } else {
      weeklyActivity.value.push({ day, lessons })
    }
  }

  const updateStatistics = (stats: Partial<UserStatistics>) => {
    statistics.value = { ...statistics.value, ...stats }
  }

  return {
    unlockedAchievements,
    weeklyActivity,
    statistics,
    unlockAchievement,
    updateWeeklyActivity,
    updateStatistics
  }
})





