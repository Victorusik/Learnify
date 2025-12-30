<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h2 class="text-h5 font-weight-bold text-primary">Learnify</h2>
          <v-btn
            variant="outlined"
            prepend-icon="mdi-plus"
            class="no-back-btn"
            @click="router.push('/learning/categories')"
          >
            Добавить курс
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="coursesStore.activeCourse">
      <v-col cols="12">
        <v-card class="course-header-card mb-4 box-shadow-1">
          <div
            class="course-background"
            :style="{ backgroundImage: `url(${coursesStore.activeCourse.cover_image_url})` }"
          >
            <div class="course-background-overlay"></div>
            <div class="course-content">
              <div class="course-icon">
                <v-icon color="white" size="large">{{ getCategoryIcon(coursesStore.activeCourse.category) }}</v-icon>
              </div>
              <div class="course-title-overlay">
                {{ coursesStore.activeCourse.title }}
              </div>
            </div>
          </div>
          <div class="course-progress-section pa-4">
            <div class="d-flex justify-space-between align-center mb-2">
              <span class="progress-label">Прогресс курса</span>
              <span class="progress-percent">{{ Math.round(coursesStore.getCourseProgress(coursesStore.activeCourse.course_id)) }}%</span>
            </div>
            <v-progress-linear
              :model-value="coursesStore.getCourseProgress(coursesStore.activeCourse.course_id)"
              color="primary"
              height="8"
              rounded
              class="mb-3"
            />
            <div class="d-flex gap-2">
              <v-btn
                color="primary"
                size="large"
                class="continue-btn mr-4"
                @click="continueCourse"
              >
                Продолжить
              </v-btn>
              <v-btn
                variant="outlined"
                size="large"
                class="no-back-btn"
                @click="router.push(`/learning/course/${coursesStore.activeCourse?.course_id}`)"
              >
                Подробнее
              </v-btn>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="coursesStore.activeCourse">
      <v-col cols="12">
        <v-card
          class="background-color-1 pa-4"
          elevation="0"
          :style="{ background: 'transparent' }"
        >
          <div class="text-h6 mb-4">Уроки курса</div>
          <div class="lessons-list">
            <div
              v-for="lesson in getLessons()"
              :key="lesson.id"
              class="lesson-item"
              :class="getLessonItemClass(lesson.id)"
              @click="openLesson(lesson.id)"
            >
              <div class="lesson-icon-wrapper">
                <div class="lesson-icon-circle" :class="getLessonIconClass(lesson.id)">
                  <v-icon
                    v-if="getLessonIconType(lesson.id) === 'check'"
                    color="white"
                    size="small"
                  >
                    mdi-check
                  </v-icon>
                  <span
                    v-else-if="getLessonIconType(lesson.id) === 'number'"
                    class="lesson-icon-number"
                  >
                    {{ lesson.order }}
                  </span>
                  <v-icon
                    v-else
                    color="#9e9e9e"
                    size="small"
                  >
                    mdi-lock
                  </v-icon>
                </div>
              </div>
              <div class="lesson-info">
                <div class="lesson-title">{{ lesson.title }}</div>
                <div class="lesson-duration">{{ getLessonDuration(lesson) }}</div>
              </div>
              <v-icon size="small" color="#757575">mdi-chevron-right</v-icon>
            </div>
          </div>
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
            @click="router.push('/learning/categories')"
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

const getLessonIconType = (lessonId: string): 'check' | 'number' | 'lock' => {
  if (coursesStore.completedLessons.includes(lessonId)) {
    return 'check'
  }
  const currentLesson = coursesStore.getCurrentLesson()
  if (currentLesson && currentLesson.id === lessonId) {
    return 'number'
  }
  return 'lock'
}

const getLessonIconClass = (lessonId: string): string => {
  if (coursesStore.completedLessons.includes(lessonId)) {
    return 'lesson-icon-completed'
  }
  const currentLesson = coursesStore.getCurrentLesson()
  if (currentLesson && currentLesson.id === lessonId) {
    return 'lesson-icon-active'
  }
  return 'lesson-icon-locked'
}

const getLessonItemClass = (lessonId: string): string => {
  if (coursesStore.completedLessons.includes(lessonId)) {
    return 'lesson-item-completed'
  }
  const currentLesson = coursesStore.getCurrentLesson()
  if (currentLesson && currentLesson.id === lessonId) {
    return 'lesson-item-active'
  }
  return 'lesson-item-locked'
}

const getLessonDuration = (lesson: any): string => {
  // Примерная длительность: ~2 минуты на блок
  const duration = lesson.blocks.length * 2
  return `${duration} мин`
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

<style scoped>
.course-header-card {
  border-radius: var(--border-radius-large);
  overflow: hidden;
}

.course-background {
  position: relative;
  height: 180px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-size: cover;
  background-position: center;
  color: white;
  overflow: hidden;
}

.course-background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.course-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  align-items: flex-end;
  padding: 16px;
}

.course-icon {
  position: absolute;
  bottom: 16px;
  left: 16px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-circle);
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-title-overlay {
  font-size: 20px;
  font-weight: 600;
  color: rgb(251, 251, 251);
  padding-left: 64px;
  line-height: 1.3;
}

.course-progress-section {
  background-color: white;
}

.progress-label {
  font-size: 14px;
  color: #424242;
  font-weight: 500;
}

.progress-percent {
  font-size: 14px;
  color: #424242;
  font-weight: 600;
}

.continue-btn {
  border: 0;
  box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
  flex: 1;
}

.details-btn {
  flex: 0 0 auto;
}

.no-back-btn {
  border: 0;
  box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}


.lessons-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--border-radius-card);
  border: 1px solid;
  cursor: pointer;
  transition: all 0.2s;
  background-color: white;
}

.lesson-item-completed {
  border-color: var(--primary-color);
}

.lesson-item-active {
  border-color: var(--primary-color);
}

.lesson-item-locked {
  border-color: #e0e0e0;
}

.lesson-icon-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lesson-icon-circle {
  width: 50px;
  height: 50px;
  border-radius: var(--border-radius-circle);
  display: flex;
  align-items: center;
  justify-content: center;
}

.lesson-icon-completed {
  background-color: var(--primary-color);
}

.lesson-icon-active {
  background-color: var(--primary-color);
}

.lesson-icon-locked {
  background-color: #f5f5f5;
}

.lesson-icon-number {
  color: white;
  font-size: 14px;
  font-weight: 600;
}

.lesson-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.lesson-title {
  font-size: 16px;
  font-weight: 500;
  color: #212121;
}

.lesson-duration {
  font-size: 14px;
  color: #757575;
}

/* Переопределение фона v-card с классом background-color-1 */
:deep(.v-card.background-color-1) {
  background: transparent !important;
  background-color: transparent !important;
}
</style>