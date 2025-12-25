<template>
  <div class="training-header pt-8">
    <div class="header-top">
      <div class="header-left">
        <div class="level-badge">
          <span>Уровень {{ userStore.level }}</span>
        </div>
        <div class="streak-badge">
          <v-icon size="small" class="streak-icon">mdi-fire</v-icon>
          <span>{{ userStore.streak }}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="greeting">Привет, {{ userStore.name }}!</div>
      </div>
    </div>
    <div class="header-bottom">
      <div class="progress-label">Сегодня: {{ userStore.completedToday }}/{{ userStore.dailyGoal }} уроков</div>
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
    <div class="progress-section">
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
  const completed = userStore.completedToday
  const goal = userStore.dailyGoal
  if (goal === 0) return 0
  return (completed / goal) * 100
})
</script>

<style scoped>
.training-header {
  background-color: var(--primary-color);
  color: white;
  padding: 16px;
  border-radius: 0 0 var(--border-radius-large) var(--border-radius-large);
  margin: -16px -16px 16px -16px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.level-badge,
.streak-badge {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-card);
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
  color: white;
}


.streak-icon {
  color: white;
}

.header-right {
  display: flex;
  align-items: flex-start;
}

.greeting {
  font-size: 16px;
  font-weight: 600;
  color: white;
  text-align: right;
}

.header-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.progress-label {
  font-size: 14px;
  color: white;
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
  width: 100%;
}

.progress-bar {
  opacity: 0.9;
}
</style>

