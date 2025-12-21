<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h2 class="text-h5">Моё обучение</h2>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            @click="$router.push('/learning/categories')"
          >
            Добавить курс
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="coursesStore.activeCourse">
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="d-flex align-center mb-2">
            <v-icon class="mr-2">{{ getCategoryIcon(coursesStore.activeCourse.category) }}</v-icon>
            <div class="text-h6">{{ coursesStore.activeCourse.title }}</div>
          </div>
          <ProgressBar
            :progress="coursesStore.getCourseProgress(coursesStore.activeCourse.course_id)"
            label="Прогресс курса"
          />
          <div class="d-flex gap-2 mt-4">
            <v-btn
              color="primary"
              @click="continueCourse"
            >
              Продолжить
            </v-btn>
            <v-btn
              variant="outlined"
              @click="$router.push(`/learning/course/${coursesStore.activeCourse?.course_id}`)"
            >
              Подробнее
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="coursesStore.activeCourse">
      <v-col cols="12">
        <v-card class="pa-4">
          <div class="text-h6 mb-4">Уроки курса</div>
          <v-list>
            <v-list-item
              v-for="lesson in getLessons()"
              :key="lesson.id"
              :prepend-icon="getLessonIcon(lesson.id)"
              :title="`${lesson.order}. ${lesson.title}`"
              :subtitle="`${lesson.blocks.length} карточек`"
              @click="openLesson(lesson.id)"
            />
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <v-card class="pa-4 text-center">
          <p>У вас нет активных курсов</p>
          <v-btn
            color="primary"
            class="mt-4"
            @click="$router.push('/learning/categories')"
          >
            Выбрать курс
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { mockCourseData } from '@/mocks/mockData'
import ProgressBar from '@/components/ui/ProgressBar.vue'

const router = useRouter()
const coursesStore = useCoursesStore()

onMounted(() => {
  // Инициализация данных курса
  if (coursesStore.availableCourses.length === 0) {
    coursesStore.availableCourses.push(mockCourseData.course)
    coursesStore.setCourseLessons('TM-INTER-002', mockCourseData.lessons)
  }
  if (coursesStore.enrolledCourses.length === 0) {
    coursesStore.enrollCourse('TM-INTER-002')
  }
})

const getLessons = () => {
  if (!coursesStore.activeCourse) return []
  return coursesStore.getCourseLessons(coursesStore.activeCourse.course_id)
}

const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    'Здоровье и продуктивность': 'mdi-run',
    'Бизнес и финансы': 'mdi-briefcase',
    'Наука': 'mdi-flask',
    'Технологии': 'mdi-laptop',
    'Мышление': 'mdi-brain'
  }
  return icons[category] || 'mdi-book'
}

const getLessonIcon = (lessonId: string) => {
  if (coursesStore.completedLessons.includes(lessonId)) {
    return 'mdi-check-circle'
  }
  const currentLesson = coursesStore.getCurrentLesson()
  if (currentLesson && currentLesson.id === lessonId) {
    return 'mdi-play-circle'
  }
  return 'mdi-lock'
}

const continueCourse = () => {
  const lesson = coursesStore.getCurrentLesson()
  if (lesson && coursesStore.activeCourse) {
    router.push(`/learning/course/${coursesStore.activeCourse.course_id}/lesson/${lesson.id}`)
  }
}

const openLesson = (lessonId: string) => {
  if (coursesStore.activeCourse) {
    router.push(`/learning/course/${coursesStore.activeCourse.course_id}/lesson/${lessonId}`)
  }
}
</script>

