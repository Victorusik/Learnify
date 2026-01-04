<template>
  <v-container>
    <v-row v-if="isLoadingLessons">
      <v-col cols="12" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-4">Загрузка информации о курсе...</p>
      </v-col>
    </v-row>
    <v-row v-else-if="loadError">
      <v-col cols="12" class="text-center py-8">
        <p class="text-error mb-4">{{ loadError }}</p>
        <v-btn color="primary" @click="router.back()">Вернуться назад</v-btn>
      </v-col>
    </v-row>
    <v-row v-else-if="course">
      <v-col cols="12">
        <v-img
          :src="course.cover_image_url"
          height="200"
          cover
          class="mb-4 border-radius-medium"
        />
        <v-chip
          :color="getLevelColor(course.level)"
          class="mb-2"
        >
          {{ course.level }}
        </v-chip>
        <h1 class="text-h5 mb-2">{{ course.title }}</h1>
        <div class="course-info mb-4">
          <div class="info-item">
            <v-icon size="small" class="mr-1">mdi-clock-outline</v-icon>
            <span>{{ course.estimated_duration_hours }} часов</span>
          </div>
          <div class="info-item">
            <v-icon size="small" class="mr-1">mdi-book-open-variant</v-icon>
            <span>{{ course.total_lessons }} уроков</span>
          </div>
          <div class="info-item">
            <v-icon size="small" class="mr-1">mdi-star</v-icon>
            <span>{{ course.total_practice_tasks }} XP</span>
          </div>
        </div>
        <p class="text-body-1 mb-4">{{ course.full_description }}</p>
        <div class="mb-4">
          <div class="text-h6 mb-2">Чему вы научитесь:</div>
          <ul>
            <li v-for="(outcome, index) in course.learning_outcomes" :key="index">
              {{ outcome }}
            </li>
          </ul>
        </div>
        <div class="mb-4">
          <div class="text-h6 mb-2">Структура курса:</div>
          <v-list class="background-transparent">
            <v-list-item
              v-for="lesson in lessons"
              :key="lesson.id"
              :title="`${lesson.order}. ${lesson.title}`"
              :subtitle="lesson.description"
            />
          </v-list>
        </div>
        <v-btn
          color="primary"
          size="large"
          block
          elevation="0"
          @click="enroll"
        >
          Записаться на курс
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { getCourseLessons } from '@/services/coursesService'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()

const courseId = route.params.id as string
const courseLessons = ref<any[]>([])

const course = computed(() => {
  return coursesStore.availableCourses.find(c => c.course_id === courseId)
})

const lessons = computed(() => {
  return courseLessons.value
})

const isLoadingLessons = ref(true)
const loadError = ref<string | null>(null)

onMounted(async () => {
  try {
    const lessonsData = await getCourseLessons(courseId)
    courseLessons.value = lessonsData
  } catch (error) {
    console.error('Failed to load course lessons:', error)
    loadError.value = 'Не удалось загрузить уроки курса'
  } finally {
    isLoadingLessons.value = false
  }
})

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

const enroll = () => {
  coursesStore.enrollCourse(courseId)
  router.push('/learning')
}
</script>

<style scoped>
.course-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #757575;
}
</style>





