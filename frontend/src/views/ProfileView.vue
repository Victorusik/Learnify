<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="profile-header">
          <h1 class="profile-title">Профиль</h1>
          <div class="profile-info d-flex align-center">
            <div class="avatar">
              {{ userStore.name.charAt(0).toUpperCase() }}
            </div>
            <div class="ml-4">
              <div class="user-name">{{ userStore.name }}</div>
              <div class="user-level">Уровень {{ userStore.level }}</div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="border-radius-large box-shadow-1 pa-4 mb-4">
          <div class="d-flex align-center mb-8">
            <v-icon size="small" color="primary" class="mr-2">mdi-chart-bar</v-icon>
            <div class="text-h6">Статистика</div>
          </div>
          <div class="statistics-grid">
            <div class="stat-item">
              <v-icon color="success" size="large" class="mb-2">mdi-book-open-variant</v-icon>
              <div class="stat-value">{{ achievementsStore.statistics.totalLessons }}</div>
              <div class="stat-label">Пройдено уроков</div>
            </div>
            <div class="stat-item">
              <v-icon color="success" size="large" class="mb-2">mdi-target</v-icon>
              <div class="stat-value">{{ achievementsStore.statistics.averageAccuracy }}%</div>
              <div class="stat-label">Средняя точность</div>
            </div>
            <div class="stat-item">
              <v-icon color="orange" size="large" class="mb-2">mdi-clock-outline</v-icon>
              <div class="stat-value">{{ achievementsStore.statistics.daysLearning }}</div>
              <div class="stat-label">Дней обучения</div>
            </div>
            <div class="stat-item">
              <v-icon color="orange" size="large" class="mb-2">mdi-fire</v-icon>
              <div class="stat-value">21</div>
              <div class="stat-label">Макс. серия</div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="border-radius-large box-shadow-1 pa-4">
          <div class="d-flex align-center mb-10">
            <v-icon size="small" color="primary" class="mr-2">mdi-cog</v-icon>
            <div class="text-h6">Настройки обучения</div>
          </div>
          <div class="mb-4">
            <div class="d-flex justify-space-between align-center mb-2">
              <span class="setting-label">Ежедневная цель</span>
              <span class="goal-value">{{ dailyGoal }} уроков</span>
            </div>
            <v-slider
              v-model="dailyGoal"
              :min="1"
              :max="10"
              :step="1"
              color="primary"
              track-color="grey-lighten-2"
              @update:model-value="updateDailyGoal"
            />
          </div>
          <div class="mb-4">
            <div class="d-flex justify-space-between align-center mb-2">
              <div class="d-flex align-center">
                <v-icon size="small" color="primary" class="mr-2">mdi-bell</v-icon>
                <span class="setting-label">Уведомления</span>
              </div>
              <v-switch
                v-model="notificationsEnabled"
                color="primary"
                hide-details
              />
            </div>
          </div>
          <div>
            <div class="setting-label mb-3">Направления обучения</div>
            <div class="categories-list">
              <v-btn
                v-for="category in categories"
                :key="category.id"
                :variant="userStore.selectedCategories.includes(category.id) ? 'elevated' : 'outlined'"
                :color="userStore.selectedCategories.includes(category.id) ? 'primary' : 'grey'"
                class="category-btn"
                @click="toggleCategory(category.id)"
              >
                <v-icon size="small" class="mr-1">{{ getCategoryIcon(category.id) }}</v-icon>
                {{ category.name }}
              </v-btn>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="border-radius-large box-shadow-1 pa-4">
          <v-btn
            color="error"
            variant="outlined"
            block
            prepend-icon="mdi-logout"
            @click="handleLogout"
          >
            Выйти
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useAchievementsStore } from '@/stores/achievementsStore'
import { mockCategories } from '@/mocks/mockData'

const router = useRouter()
const userStore = useUserStore()
const achievementsStore = useAchievementsStore()

const dailyGoal = ref(userStore.dailyGoal)
const notificationsEnabled = ref(true)
const categories = mockCategories


const getCategoryIcon = (categoryId: string): string => {
  const iconMap: Record<string, string> = {
    'business': 'mdi-briefcase',
    'science': 'mdi-microscope',
    'tech': 'mdi-laptop',
    'health': 'mdi-heart',
    'mindset': 'mdi-brain'
  }
  return iconMap[categoryId] || 'mdi-book'
}

const updateDailyGoal = (value: number) => {
  userStore.updateDailyGoal(value)
}

const toggleCategory = (categoryId: string) => {
  userStore.toggleCategory(categoryId)
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.profile-header {
  margin-bottom: 24px;
}

.profile-title {
  font-size: 20px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 16px;
  color: #212121;
}

.profile-info {
  padding: 16px 0;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: var(--border-radius-circle);
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  flex-shrink: 0;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #212121;
}

.user-level {
  font-size: 14px;
  color: #757575;
  margin-top: 4px;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #212121;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #757575;
}

.setting-label {
  font-size: 14px;
  font-weight: 500;
  color: #424242;
}

.goal-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color);
}

.notification-times {
  font-size: 14px;
  color: #757575;
  margin-top: 8px;
}

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-btn {
  text-transform: none;
  letter-spacing: normal;
}
</style>





