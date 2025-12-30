<template>
  <v-card class="completion-card" elevation="4">
    <v-card-text class="text-center pa-8">
      <div class="completion-icon mb-6">
        <v-icon size="80" color="success">mdi-check-circle</v-icon>
      </div>

      <h2 class="text-h4 mb-2 font-weight-bold">Урок завершён! 🎉</h2>
      <p class="text-body-1 text-medium-emphasis mb-6">
        Отличная работа! Вы успешно прошли урок "{{ lessonTitle }}"
      </p>

      <v-divider class="mb-6" />

      <div class="stats-container mb-6">
        <div class="stat-item">
          <v-icon size="24" color="primary" class="mb-2">mdi-check-all</v-icon>
          <div class="text-h6 font-weight-bold">{{ completedBlocks }}/{{ totalBlocks }}</div>
          <div class="text-caption text-medium-emphasis">Карточек пройдено</div>
        </div>
        <v-divider vertical />
        <div class="stat-item">
          <v-icon size="24" color="warning" class="mb-2">mdi-star</v-icon>
          <div class="text-h6 font-weight-bold">+{{ xpEarned }}</div>
          <div class="text-caption text-medium-emphasis">Опыт получено</div>
        </div>
        <v-divider vertical />
        <div class="stat-item">
          <v-icon size="24" color="success" class="mb-2">mdi-progress-check</v-icon>
          <div class="text-h6 font-weight-bold">{{ Math.round(progress) }}%</div>
          <div class="text-caption text-medium-emphasis">Прогресс урока</div>
        </div>
      </div>

      <v-divider class="mb-6" />

      <div class="actions-container">
        <v-btn
          v-if="hasNextLesson"
          color="primary"
          size="large"
          prepend-icon="mdi-arrow-right"
          @click="$emit('next-lesson')"
          class="mb-3"
          block
        >
          Следующий урок
        </v-btn>
        <v-btn
          color="default"
          variant="text"
          size="large"
          prepend-icon="mdi-home"
          @click="$emit('back-to-learning')"
          block
        >
          На главную
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  lessonTitle: string
  completedBlocks: number
  totalBlocks: number
  progress: number
  xpEarned: number
  hasNextLesson: boolean
}>()

defineEmits<{
  'next-lesson': []
  'back-to-course': []
  'back-to-learning': []
}>()
</script>

<style scoped>
.completion-card {
  max-width: 600px;
  margin: 0 auto;
  border-radius: 16px;
}

.completion-icon {
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.stats-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 16px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
}

.actions-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (max-width: 600px) {
  .stats-container {
    flex-direction: column;
    gap: 8px;
  }

  .stat-item {
    width: 100%;
    padding: 16px;
  }

  .stats-container :deep(.v-divider--vertical) {
    display: none;
  }
}
</style>

