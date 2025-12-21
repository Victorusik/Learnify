<template>
  <v-container>
    <v-row v-if="course">
      <v-col cols="12">
        <v-img
          :src="course.cover_image_url"
          height="300"
          cover
          class="mb-4"
        />
        <v-chip
          :color="getLevelColor(course.level)"
          class="mb-2"
        >
          {{ course.level }}
        </v-chip>
        <h1 class="text-h4 mb-2">{{ course.title }}</h1>
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
          <div class="text-h6 mb-2">Требования:</div>
          <ul>
            <li v-for="(req, index) in course.prerequisites" :key="index">
              {{ req }}
            </li>
          </ul>
        </div>
        <div class="mb-4">
          <div class="text-h6 mb-2">Структура курса:</div>
          <v-list>
            <v-list-item
              v-for="lesson in lessons"
              :key="lesson.id"
              :title="`${lesson.order}. ${lesson.title}`"
              :subtitle="`${lesson.blocks.length} блоков`"
            />
          </v-list>
        </div>
        <v-btn
          color="primary"
          size="large"
          block
          @click="enroll"
        >
          Записаться на курс
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { mockCourseData } from '@/mocks/mockData'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()

const courseId = route.params.id as string

const course = computed(() => {
  return coursesStore.availableCourses.find(c => c.course_id === courseId) || mockCourseData.course
})

const lessons = computed(() => {
  return mockCourseData.lessons
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



