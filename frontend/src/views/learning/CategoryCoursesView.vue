<template>
  <v-container>
    <v-row v-if="isLoading">
      <v-col cols="12" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-4">Загрузка курсов...</p>
      </v-col>
    </v-row>
    <v-row v-else-if="loadError">
      <v-col cols="12" class="text-center py-8">
        <p class="text-error mb-4">{{ loadError }}</p>
        <v-btn color="primary" @click="router.back()">Вернуться назад</v-btn>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            class="mr-2"
            @click="router.back()"
          />
          <h2 class="text-h5">{{ categoryName }}</h2>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="course in categoryCourses"
        :key="course.course_id"
        cols="12"
        class="d-flex"
      >
        <CourseCard
          class="flex-grow-1"
          :course="course"
          @details="goToCourse(course.course_id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { getCategories } from '@/services/categoriesService'
import { getCourses } from '@/services/coursesService'
import CourseCard from '@/components/ui/CourseCard.vue'
import type { Category } from '@/types'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()

const categoryId = route.params.id as string
const categories = ref<Category[]>([])

const category = computed(() => {
  return categories.value.find(c => c.id === categoryId)
})

const categoryName = computed(() => {
  return category.value?.name || 'Категория'
})

const categoryCourses = computed(() => {
  // Фильтруем курсы по категории
  return coursesStore.availableCourses.filter(course => {
    if (!category.value) return false
    return course.category === category.value.name
  })
})

const isLoading = ref(true)
const loadError = ref<string | null>(null)

onMounted(async () => {
  try {
    // Загружаем категории
    const categoriesData = await getCategories()
    categories.value = categoriesData

    // Загружаем курсы если еще не загружены
    if (coursesStore.availableCourses.length === 0) {
      const coursesResponse = await getCourses()
      // Transform CourseResponse to Course by converting category object to string
      const courses = coursesResponse.map(course => ({
        ...course,
        category: course.category?.name || 'Без категории'
      }))
      coursesStore.availableCourses = courses
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    loadError.value = 'Не удалось загрузить курсы'
  } finally {
    isLoading.value = false
  }
})

const goToCourse = (courseId: string) => {
  router.push(`/learning/course/${courseId}`)
}
</script>





