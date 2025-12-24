<template>
  <div class="training-header">
    <div class="header-content">
      <div class="header-left">
        <div class="level-info">
          <span class="level-text">Уровень {{ userStore.level }}</span>
          <div class="streak-info">
            <v-icon size="small" class="streak-icon">mdi-hourglass</v-icon>
            <span class="streak-text">{{ userStore.streak }} дней</span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <div class="greeting">Привет, {{ userStore.name }}!</div>
        <v-btn
          size="small"
          variant="text"
          class="change-goal-btn"
          prepend-icon="mdi-cog"
          @click="$emit('change-goal')"
        >
          Изменить цель
        </v-btn>
      </div>
    </div>
    <div class="progress-section">
      <div class="progress-label">Сегодня: {{ userStore.completedToday }}/{{ userStore.dailyGoal }} уроков</div>
      <v-progress-linear
        :model-value="dailyProgress"
        color="white"
        height="8"
        rounded
        class="progress-bar"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()

defineEmits<{
  'change-goal': []
}>()

const dailyProgress = computed(() => {
  if (userStore.dailyGoal === 0) return 0
  return (userStore.completedToday / userStore.dailyGoal) * 100
})
</script>

<style scoped>
.training-header {
  background-color: var(--primary-color);
  color: white;
  padding: 16px;
  border-radius: 0 0 16px 16px;
  margin: -16px -16px 16px -16px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.level-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.level-text {
  font-size: 16px;
  font-weight: 600;
  color: white;
}

.streak-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.streak-icon {
  color: white;
}

.streak-text {
  font-size: 14px;
  color: white;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.greeting {
  font-size: 16px;
  font-weight: 600;
  color: white;
  text-align: right;
}

.change-goal-btn {
  color: white !important;
  min-width: auto;
  padding: 4px 8px;
}

.change-goal-btn :deep(.v-btn__prepend) {
  margin-inline-end: 4px;
}

.progress-section {
  margin-top: 12px;
}

.progress-label {
  font-size: 14px;
  color: white;
  margin-bottom: 8px;
}

.progress-bar {
  opacity: 0.9;
}
</style>

