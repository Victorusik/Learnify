import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const name = ref('Алексей')
  const level = ref(12)
  const xp = ref(1245)
  const streak = ref(14)
  const dailyGoal = ref(5)
  const completedToday = ref(3)
  const selectedCategories = ref<string[]>(['health', 'tech'])


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

  const updateNotifications = (times: { time: string }[]) => {
    notifications.value = times
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
  }

  const resetStreak = () => {
    streak.value = 0
  }

  return {
    name,
    level,
    xp,
    streak,
    dailyGoal,
    completedToday,
    selectedCategories,
    xpToNextLevel,
    xpProgress,
    addXP,
    updateDailyGoal,
    updateNotifications,
    toggleCategory,
    incrementStreak,
    resetStreak
  }
})





