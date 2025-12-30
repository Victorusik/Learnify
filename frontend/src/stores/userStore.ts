import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { format } from 'date-fns'

export const useUserStore = defineStore('user', () => {
  const name = ref('Алексей')
  const level = ref(1)
  const xp = ref(0)
  const streak = ref(1)
  const dailyGoal = ref(5)
  const completedToday = ref(0)
  const selectedCategories = ref<string[]>(['health', 'tech'])
  const lastStreakUpdateDate = ref<string | null>(null)


  const xpToNextLevel = computed(() => {
    const xpForCurrentLevel = level.value * 100
    const currentLevelXp = xp.value - ((level.value - 1) * 100)
    return xpForCurrentLevel - currentLevelXp
  })

  const xpProgress = computed(() => {
    const xpForCurrentLevel = level.value * 100
    const currentLevelXp = xp.value - ((level.value - 1) * 100)
    return (currentLevelXp / xpForCurrentLevel) * 100
  })

  const addXP = (amount: number) => {
    xp.value += amount
    const newLevel = Math.floor(xp.value / 100) + 1
    if (newLevel > level.value) {
      level.value = newLevel
    }
  }

  const updateDailyGoal = (goal: number) => {
    dailyGoal.value = goal
  }

  const toggleCategory = (categoryId: string) => {
    const index = selectedCategories.value.indexOf(categoryId)
    if (index > -1) {
      selectedCategories.value.splice(index, 1)
    } else {
      selectedCategories.value.push(categoryId)
    }
  }

  const incrementStreak = () => {
    streak.value += 1
    lastStreakUpdateDate.value = format(new Date(), 'yyyy-MM-dd')
  }

  const resetStreak = () => {
    streak.value = 0
  }

  const incrementCompletedToday = () => {
    completedToday.value += 1

    // Проверяем, достигнута ли цель и не был ли стрик уже увеличен сегодня
    const today = format(new Date(), 'yyyy-MM-dd')
    const wasStreakUpdatedToday = lastStreakUpdateDate.value === today

    if (completedToday.value >= dailyGoal.value && !wasStreakUpdatedToday) {
      incrementStreak()
      lastStreakUpdateDate.value = today
    }
  }

  return {
    name,
    level,
    xp,
    streak,
    dailyGoal,
    completedToday,
    selectedCategories,
    lastStreakUpdateDate,
    xpToNextLevel,
    xpProgress,
    addXP,
    updateDailyGoal,
    toggleCategory,
    incrementStreak,
    resetStreak,
    incrementCompletedToday
  }
})





