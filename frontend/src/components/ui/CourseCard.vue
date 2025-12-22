<template>
  <v-card
    :elevation="3"
    class="course-card"
    :style="{ borderRadius: 'var(--card-border-radius)' }"
  >
    <v-img
      :src="course.cover_image_url"
      height="200"
      cover
    >
      <v-chip
        :color="getLevelColor(course.level)"
        class="ma-2"
        size="small"
      >
        {{ course.level }}
      </v-chip>
    </v-img>
    <v-card-title>{{ course.title }}</v-card-title>
    <v-card-subtitle>{{ course.short_description }}</v-card-subtitle>
    <v-card-text>
      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="mr-1">mdi-clock-outline</v-icon>
        <span class="text-caption">{{ course.estimated_duration_hours }} часов</span>
      </div>
      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="mr-1">mdi-book-open-variant</v-icon>
        <span class="text-caption">{{ course.total_lessons }} уроков</span>
      </div>
      <div class="d-flex align-center">
        <v-icon size="small" class="mr-1">mdi-star</v-icon>
        <span class="text-caption">{{ course.total_practice_tasks }} XP за завершение</span>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="primary"
        variant="text"
        @click="$emit('details')"
      >
        Подробнее
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import type { Course } from '@/types'

defineProps<{
  course: Course
}>()

defineEmits<{
  details: []
}>()

const getLevelColor = (level: string) => {
  switch (level) {
    case 'Легкий':
      return 'success'
    case 'Средний':
      return 'warning'
    case 'Сложный':
      return 'error'
    default:
      return 'primary'
  }
}
</script>

<style scoped>
.course-card {
  height: 100%;
}
</style>