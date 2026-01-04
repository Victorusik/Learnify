import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import type { UserProfile } from '@/types'
import * as authService from '@/services/authService'

export const useUserStore = defineStore('user', () => {
  const user = ref<UserProfile | null>(null)
  const lastStreakUpdateDate = ref<string | null>(null)

  const name = computed(() => user.value?.name || '')
  const level = computed(() => user.value?.level || 1)
  const xp = computed(() => user.value?.xp || 0)
  const streak = computed(() => user.value?.streak || 0)
  const dailyGoal = computed(() => user.value?.daily_goal || 5)
  const completedToday = computed(() => user.value?.completed_today || 0)
  const selectedCategories = computed(() => user.value?.selected_categories || [])

  const isAuthenticated = computed(() => authService.isAuthenticated())


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
    if (!user.value) return
    user.value.xp += amount
    const newLevel = Math.floor(user.value.xp / 100) + 1
    if (newLevel > user.value.level) {
      user.value.level = newLevel
    }
  }

  const updateDailyGoal = (goal: number) => {
    if (!user.value) return
    user.value.daily_goal = goal
  }

  const toggleCategory = (categoryId: string) => {
    if (!user.value) return
    const index = user.value.selected_categories.indexOf(categoryId)
    if (index > -1) {
      user.value.selected_categories.splice(index, 1)
    } else {
      user.value.selected_categories.push(categoryId)
    }
  }

  const incrementStreak = () => {
    if (!user.value) return
    user.value.streak += 1
    lastStreakUpdateDate.value = format(new Date(), 'yyyy-MM-dd')
  }

  const resetStreak = () => {
    if (!user.value) return
    user.value.streak = 0
  }

  const incrementCompletedToday = () => {
    if (!user.value) return

    user.value.completed_today += 1

    const today = format(new Date(), 'yyyy-MM-dd')
    const wasStreakUpdatedToday = lastStreakUpdateDate.value === today

    if (user.value.completed_today >= user.value.daily_goal && !wasStreakUpdatedToday) {
      incrementStreak()
      lastStreakUpdateDate.value = today
    }
  }

  const login = async (email: string, password: string) => {
    await authService.login(email, password)
  }

  const register = async (email: string, password: string, name: string) => {
    await authService.register(email, password, name)
  }

  const logout = () => {
    authService.logout()
    user.value = null
    lastStreakUpdateDate.value = null
  }

  const fetchProfile = async () => {
    if (!authService.isAuthenticated()) {
      user.value = null
      return
    }

    try {
      const profile = await authService.getProfile()
      user.value = profile
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error)
      user.value = null
    }
  }

  return {
    user,
    name,
    level,
    xp,
    streak,
    dailyGoal,
    completedToday,
    selectedCategories,
    lastStreakUpdateDate,
    isAuthenticated,
    xpToNextLevel,
    xpProgress,
    addXP,
    updateDailyGoal,
    toggleCategory,
    incrementStreak,
    resetStreak,
    incrementCompletedToday,
    login,
    register,
    logout,
    fetchProfile
  }
})





