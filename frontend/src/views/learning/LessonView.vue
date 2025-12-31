<template>
  <v-container>
    <v-row v-if="isLoadingLesson">
      <v-col cols="12" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-4">Загрузка урока...</p>
      </v-col>
    </v-row>
    <v-row v-else-if="lessonLoadError">
      <v-col cols="12" class="text-center py-8">
        <p class="text-error mb-4">{{ lessonLoadError }}</p>
        <v-btn color="primary" @click="loadLessonData">Попробовать снова</v-btn>
      </v-col>
    </v-row>
    <v-row v-else-if="lesson">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6">
          <div>
            <div class="text-subtitle-2">{{ lesson.title }} ({{ lesson.order }}/{{ totalLessons }})</div>
          </div>
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            @click="$router.back()"
          />
        </div>
        <ProgressBar
          :progress="progress"
          :completed-blocks="completedBlocks"
          :total-blocks="totalBlocks"
        />
      </v-col>
    </v-row>
    <v-row v-if="currentBlock">
      <v-col cols="12">
        <component
          :is="getBlockComponent(currentBlock)"
          :block="currentBlock"
          @answer-submitted="handleAnswer"
          @next="nextBlock"
        />
      </v-col>
    </v-row>
    <v-row v-else-if="lesson">
      <v-col cols="12">
        <LessonCompletionScreen
          :lesson-title="lesson.title"
          :completed-blocks="completedBlocks"
          :total-blocks="totalBlocks"
          :progress="progress"
          :xp-earned="10"
          :has-next-lesson="hasNextLesson"
          @next-lesson="goToNextLesson"
          @back-to-course="goToCourse"
          @back-to-learning="completeLesson"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useCoursesStore } from '@/stores/coursesStore'
import { useUserStore } from '@/stores/userStore'
import { useCardsStore } from '@/stores/cardsStore'
import type { Block, Lesson } from '@/types'
import { markBlockCompleted, markLessonCompleted } from '@/services/progressService'
import { getLesson } from '@/services/lessonsService'
import { getCourseLessons } from '@/services/coursesService'
import TheoryCard from '@/components/cards/TheoryCard.vue'
import PracticeMultipleChoice from '@/components/cards/PracticeMultipleChoice.vue'
import PracticeReflection from '@/components/cards/PracticeReflection.vue'
import PracticeCase from '@/components/cards/PracticeCase.vue'
import PracticeTextInput from '@/components/cards/PracticeTextInput.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import LessonCompletionScreen from '@/components/ui/LessonCompletionScreen.vue'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()
const userStore = useUserStore()

const lessonId = computed(() => route.params.lessonId as string)
const courseId = computed(() => route.params.courseId as string)

const lesson = ref<Lesson | null>(null)
const courseLessons = ref<any[]>([])
const isLoadingLesson = ref(true)
const lessonLoadError = ref<string | null>(null)

const totalLessons = computed(() => {
  return courseLessons.value.length
})

const currentBlockIndex = ref(0)
const currentBlock = computed(() => {
  if (!lesson.value) return null
  return lesson.value.blocks[currentBlockIndex.value] || null
})

const totalBlocks = computed(() => {
  return lesson.value?.blocks.length || 0
})

const completedBlocks = computed(() => {
  // Отслеживаем изменения Map через обращение к value
  return coursesStore.lessonsProgress.get(lessonId.value) || 0
})

const progress = computed(() => {
  if (totalBlocks.value === 0) return 0
  return (completedBlocks.value / totalBlocks.value) * 100
})

const hasNextLesson = computed(() => {
  if (!lesson.value) return false
  return lesson.value.order < totalLessons.value
})

const nextLesson = computed(() => {
  if (!lesson.value || !hasNextLesson.value) return null
  return courseLessons.value.find(l => l.order === lesson.value!.order + 1)
})

const getBlockComponent = (block: Block) => {
  if (block.type === 'theory') return TheoryCard
  if (block.type === 'practice') {
    switch (block.subtype) {
      case 'multiple_choice':
        return PracticeMultipleChoice
      case 'reflection':
        return PracticeReflection
      case 'case':
        return PracticeCase
      case 'text_input':
        return PracticeTextInput
    }
  }
  return TheoryCard
}

const cardsStore = useCardsStore()
const processedBlocks = ref<Set<number>>(new Set())
const savingProgress = ref(false)

// Генерирует ID блока если его нет (для mock данных)
const getBlockId = (block: Block): string => {
  return block.id || `${lessonId.value}_block_${block.order}`
}

const handleAnswer = async (isCorrect: boolean) => {
  if (currentBlock.value && !savingProgress.value) {
    const blockOrder = currentBlock.value.order
    if (!processedBlocks.value.has(blockOrder)) {
      try {
        savingProgress.value = true
        const blockId = getBlockId(currentBlock.value)

        // Отправляем прогресс на бэкенд
        await markBlockCompleted({
          block_id: blockId,
          lesson_id: lessonId.value,
          course_id: courseId.value
        })

        // Обновляем локальное состояние после успешного сохранения
        coursesStore.markBlockCompleted(lessonId.value)
        processedBlocks.value.add(blockOrder)
      } catch (error) {
        console.error('Failed to save block progress:', error)
        // Показываем ошибку пользователю, но продолжаем работу
        alert('Не удалось сохранить прогресс. Проверьте подключение к интернету.')
      } finally {
        savingProgress.value = false
      }
    }

    if (!isCorrect) {
      // Помечаем карточку для повторения
      const blockId = getBlockId(currentBlock.value)
      cardsStore.submitAnswer(blockId, false, lessonId.value, courseId.value)
    }
  }
}

const nextBlock = async () => {
  // Обновляем прогресс для карточек, которые еще не были обработаны
  if (currentBlock.value && !savingProgress.value) {
    const blockOrder = currentBlock.value.order
    if (!processedBlocks.value.has(blockOrder)) {
      try {
        savingProgress.value = true
        const blockId = getBlockId(currentBlock.value)

        // Отправляем прогресс на бэкенд
        await markBlockCompleted({
          block_id: blockId,
          lesson_id: lessonId.value,
          course_id: courseId.value
        })

        // Карточка еще не обработана (теория или практика без answer-submitted)
        coursesStore.markBlockCompleted(lessonId.value)
        processedBlocks.value.add(blockOrder)
      } catch (error) {
        console.error('Failed to save block progress:', error)
        alert('Не удалось сохранить прогресс. Проверьте подключение к интернету.')
      } finally {
        savingProgress.value = false
      }
    }
  }

  // Переходим к следующему блоку или завершаем урок
  if (currentBlockIndex.value < totalBlocks.value - 1) {
    currentBlockIndex.value++
  } else {
    // Если это последний блок, увеличиваем индекс за пределы массива,
    // чтобы currentBlock стал null и показался экран завершения
    currentBlockIndex.value = totalBlocks.value
  }
}

const completeLesson = async () => {
  try {
    // Отправляем завершение урока на бэкенд
    await markLessonCompleted({
      lesson_id: lessonId.value,
      course_id: courseId.value
    })

    coursesStore.completeLesson(lessonId.value)
    userStore.addXP(10)
    userStore.incrementCompletedToday()
    router.push('/learning')
  } catch (error) {
    console.error('Failed to complete lesson:', error)
    alert('Не удалось сохранить завершение урока. Проверьте подключение к интернету.')
  }
}

const goToNextLesson = async () => {
  if (nextLesson.value) {
    try {
      // Отправляем завершение урока на бэкенд
      await markLessonCompleted({
        lesson_id: lessonId.value,
        course_id: courseId.value
      })

      coursesStore.completeLesson(lessonId.value)
      userStore.addXP(10)
      userStore.incrementCompletedToday()
      router.push(`/learning/course/${courseId.value}/lesson/${nextLesson.value.id}`)
    } catch (error) {
      console.error('Failed to complete lesson:', error)
      alert('Не удалось сохранить завершение урока. Проверьте подключение к интернету.')
    }
  }
}

const goToCourse = async () => {
  try {
    // Отправляем завершение урока на бэкенд
    await markLessonCompleted({
      lesson_id: lessonId.value,
      course_id: courseId.value
    })

    coursesStore.completeLesson(lessonId.value)
    userStore.addXP(10)
    userStore.incrementCompletedToday()
    router.push(`/learning/course/${courseId.value}`)
  } catch (error) {
    console.error('Failed to complete lesson:', error)
    alert('Не удалось сохранить завершение урока. Проверьте подключение к интернету.')
  }
}

const loadLessonData = async () => {
  isLoadingLesson.value = true
  lessonLoadError.value = null

  try {
    // Загружаем данные урока
    const lessonData = await getLesson(lessonId.value)
    lesson.value = lessonData

    // Загружаем список уроков курса для навигации
    try {
      const lessons = await getCourseLessons(courseId.value)
      courseLessons.value = lessons
    } catch (error) {
      console.error('Failed to load course lessons:', error)
      // Продолжаем работу даже если не удалось загрузить список уроков
    }

    // Инициализируем урок
    coursesStore.currentLesson = lessonData
    cardsStore.initializeBlocks(lessonData.blocks)
    currentBlockIndex.value = 0
    processedBlocks.value = new Set()
  } catch (error) {
    console.error('Failed to load lesson:', error)
    lessonLoadError.value = 'Не удалось загрузить урок. Проверьте подключение к интернету.'
  } finally {
    isLoadingLesson.value = false
  }
}

const initializeLesson = () => {
  loadLessonData()
}

// Отслеживаем изменения lessonId и сбрасываем состояние
watch(lessonId, () => {
  initializeLesson()
}, { immediate: false })

// Обрабатываем обновление маршрута (когда переходим на новый урок)
onBeforeRouteUpdate((to) => {
  const newLessonId = to.params.lessonId as string
  if (newLessonId !== lessonId.value) {
    initializeLesson()
  }
})

onMounted(() => {
  initializeLesson()
})
</script>

