<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2 class="text-h5 mb-4">{{ categoryName }}</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="course in categoryCourses"
        :key="course.course_id"
        cols="12"
        sm="6"
        md="4"
      >
        <CourseCard
          :course="course"
          @details="goToCourse(course.course_id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { mockCourseData, mockAdditionalCourses, mockCategories } from '@/mocks/mockData'
import CourseCard from '@/components/ui/CourseCard.vue'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()

const categoryId = route.params.id as string

const category = computed(() => {
  return mockCategories.find(c => c.id === categoryId)
})

const categoryName = computed(() => {
  return category.value?.name || 'Категория'
})

const categoryCourses = computed(() => {
  const allCourses = [mockCourseData.course, ...mockAdditionalCourses]
  return allCourses.filter(course => {
    if (categoryId === 'health') {
      return course.category === 'Здоровье и продуктивность'
    }
    if (categoryId === 'business') {
      return course.category === 'Бизнес и финансы'
    }
    if (categoryId === 'science') {
      return course.category === 'Наука'
    }
    if (categoryId === 'tech') {
      return course.category === 'Технологии'
    }
    if (categoryId === 'mindset') {
      return course.category === 'Мышление'
    }
    return false
  })
})

const goToCourse = (courseId: string) => {
  router.push(`/learning/course/${courseId}`)
}
</script>




