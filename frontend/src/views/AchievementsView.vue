<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="border-radius-large box-shadow-1 pa-4 mb-4">
          <div class="d-flex align-center">
            <CircularProgressBar
              :progress="userStore.xpProgress"
              :size="80"
            />
            <div class="user-info ml-5">
              <div class="user-name">
                {{ userStore.name }} (Уровень {{ userStore.level }})
              </div>
              <div class="user-xp mt-2">
                Всего опыта: {{ userStore.xp }} XP
              </div>
              <div class="user-xp-next mt-1">
                До следующего уровня: {{ userStore.xpToNextLevel }} XP
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="border-radius-large box-shadow-1 pa-4 mb-4">
          <div class="d-flex align-center mb-3">
            <v-icon size="small" color="orange" class="mr-2">mdi-fire</v-icon>
            <div class="text-h6">Серия дней</div>
          </div>
          <div class="d-flex justify-space-between mb-4">
            <div>
              <div class="streak-value">{{ userStore.streak }} дней</div>
              <div class="streak-label">Текущая серия</div>
            </div>
            <div class="text-right">
              <div class="streak-value">21 дней</div>
              <div class="streak-label">Рекорд</div>
            </div>
          </div>
          <div class="calendar-section">
            <div class="calendar-title mb-3">Последние 4 недели</div>
            <ActivityCalendar :activity-data="activityMap" />
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useAchievementsStore } from '@/stores/achievementsStore'
import CircularProgressBar from '@/components/ui/CircularProgressBar.vue'
import ActivityCalendar from '@/components/ui/ActivityCalendar.vue'
import { subDays, format } from 'date-fns'

const userStore = useUserStore()
const achievementsStore = useAchievementsStore()

// Генерируем данные активности для календаря на основе текущей серии
const activityMap = computed(() => {
  const map = new Map<string, boolean>()
  const today = new Date()

  // Помечаем только дни текущей серии как активные
  for (let i = 0; i < userStore.streak && i < 28; i++) {
    const date = subDays(today, i)
    const dateKey = format(date, 'yyyy-MM-dd')
    map.set(dateKey, true)
  }

  return map
})
</script>

<style scoped>
.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #212121;
}

.user-xp,
.user-xp-next {
  font-size: 14px;
  color: #757575;
}

.streak-value {
  font-size: 24px;
  font-weight: 600;
  color: #212121;
  line-height: 1.2;
}

.streak-label {
  font-size: 14px;
  color: #757575;
  margin-top: 4px;
}

.calendar-section {
  margin-top: 16px;
}

.calendar-title {
  font-size: 14px;
  font-weight: 500;
  color: #424242;
}
</style>





