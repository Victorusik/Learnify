<template>
  <v-container>
    <v-row v-if="lesson">
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
import { mockCourseData } from '@/mocks/mockData'
import type { Block } from '@/types'
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

const lesson = computed(() => {
  return mockCourseData.lessons.find(l => l.id === lessonId.value)
})

const totalLessons = computed(() => {
  return mockCourseData.lessons.length
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
  return mockCourseData.lessons.find(l => l.order === lesson.value!.order + 1)
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

const handleAnswer = (isCorrect: boolean) => {
  if (currentBlock.value) {
    // Обновляем прогресс для практики с ответом
    const blockOrder = currentBlock.value.order
    if (!processedBlocks.value.has(blockOrder)) {
      coursesStore.markBlockCompleted(lessonId.value)
      processedBlocks.value.add(blockOrder)
    }
    if (!isCorrect) {
      // Помечаем карточку для повторения
      const blockId = `${currentBlock.value.type}-${currentBlock.value.order}`
      cardsStore.submitAnswer(blockId, false, lessonId.value, courseId.value)
    }
  }
}

const nextBlock = () => {
  // Обновляем прогресс для карточек, которые еще не были обработаны
  if (currentBlock.value) {
    const blockOrder = currentBlock.value.order
    if (!processedBlocks.value.has(blockOrder)) {
      // Карточка еще не обработана (теория или практика без answer-submitted)
      coursesStore.markBlockCompleted(lessonId.value)
      processedBlocks.value.add(blockOrder)
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

const completeLesson = () => {
  coursesStore.completeLesson(lessonId.value)
  userStore.addXP(10)
  userStore.incrementCompletedToday()
  router.push('/learning')
}

const goToNextLesson = () => {
  if (nextLesson.value) {
    coursesStore.completeLesson(lessonId.value)
    userStore.addXP(10)
    userStore.incrementCompletedToday()
    router.push(`/learning/course/${courseId.value}/lesson/${nextLesson.value.id}`)
  }
}

const goToCourse = () => {
  coursesStore.completeLesson(lessonId.value)
  userStore.addXP(10)
  userStore.incrementCompletedToday()
  router.push(`/learning/course/${courseId.value}`)
}

const initializeLesson = () => {
  if (lesson.value) {
    coursesStore.currentLesson = lesson.value
    // Инициализируем блоки для тренировки
    cardsStore.initializeBlocks(lesson.value.blocks)
    // Сбрасываем индекс блока и обработанные блоки
    currentBlockIndex.value = 0
    processedBlocks.value = new Set()
  }
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

