<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="text-h6 mb-4">Статистика</div>
          <div class="mb-2">Всего пройдено уроков: {{ achievementsStore.statistics.totalLessons }}</div>
          <div class="mb-2">Средняя точность: {{ achievementsStore.statistics.averageAccuracy }}%</div>
          <div>Дней обучения: {{ achievementsStore.statistics.daysLearning }}</div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <div class="text-h6 mb-4">Настройки обучения</div>
          <div class="mb-4">
            <div class="mb-2">Ежедневная цель: {{ userStore.dailyGoal }} уроков</div>
            <v-slider
              v-model="dailyGoal"
              :min="1"
              :max="10"
              :step="1"
              thumb-label
              @update:model-value="updateDailyGoal"
            />
          </div>
          <div class="mb-4">
            <div class="mb-2">Уведомления:</div>
            <v-chip
              v-for="(notif, index) in userStore.notifications"
              :key="index"
              class="mr-2"
            >
              {{ notif.time }}
            </v-chip>
          </div>
          <div>
            <div class="mb-2">Направления:</div>
            <v-chip
              v-for="category in categories"
              :key="category.id"
              :color="userStore.selectedCategories.includes(category.id) ? 'primary' : 'default'"
              class="mr-2 mb-2"
              @click="toggleCategory(category.id)"
            >
              {{ category.icon }} {{ category.name }}
            </v-chip>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useAchievementsStore } from '@/stores/achievementsStore'
import { mockCategories } from '@/mocks/mockData'

const userStore = useUserStore()
const achievementsStore = useAchievementsStore()

const dailyGoal = ref(userStore.dailyGoal)
const categories = mockCategories

const updateDailyGoal = (value: number) => {
  userStore.updateDailyGoal(value)
}

const toggleCategory = (categoryId: string) => {
  userStore.toggleCategory(categoryId)
}
</script>



