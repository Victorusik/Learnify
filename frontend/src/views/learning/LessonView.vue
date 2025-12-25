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
        <v-card class="pa-4 text-center">
          <p class="text-h6 mb-4">Урок завершён! 🎉</p>
          <v-btn
            color="primary"
            @click="completeLesson"
          >
            Завершить урок
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()
const userStore = useUserStore()

const lessonId = route.params.lessonId as string
const courseId = route.params.courseId as string

const lesson = computed(() => {
  return mockCourseData.lessons.find(l => l.id === lessonId)
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
  return coursesStore.lessonsProgress.get(lessonId) || 0
})

const progress = computed(() => {
  if (totalBlocks.value === 0) return 0
  return (completedBlocks.value / totalBlocks.value) * 100
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
      coursesStore.markBlockCompleted(lessonId)
      processedBlocks.value.add(blockOrder)
    }
    if (!isCorrect) {
      // Помечаем карточку для повторения
      const blockId = `${currentBlock.value.type}-${currentBlock.value.order}`
      cardsStore.submitAnswer(blockId, false, lessonId, courseId)
    }
  }
}

const nextBlock = () => {
  // Обновляем прогресс для карточек, которые еще не были обработаны
  if (currentBlock.value) {
    const blockOrder = currentBlock.value.order
    if (!processedBlocks.value.has(blockOrder)) {
      // Карточка еще не обработана (теория или практика без answer-submitted)
      coursesStore.markBlockCompleted(lessonId)
      processedBlocks.value.add(blockOrder)
    }
  }

  if (currentBlockIndex.value < totalBlocks.value - 1) {
    currentBlockIndex.value++
  }
}

const completeLesson = () => {
  coursesStore.completeLesson(lessonId)
  userStore.addXP(10)
  router.push('/learning')
}

onMounted(() => {
  if (lesson.value) {
    coursesStore.currentLesson = lesson.value
    // Инициализируем блоки для тренировки
    const cardsStore = useCardsStore()
    cardsStore.initializeBlocks(lesson.value.blocks)
  }
})
</script>

