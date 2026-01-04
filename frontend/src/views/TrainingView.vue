<template>
  <v-container class="training-container">
    <TrainingHeader @change-goal="router.push('/profile')" />
    <v-row>
      <v-col cols="12">
        <v-card v-if="isLoading" class="pa-4 text-center">
          <v-progress-circular indeterminate color="primary" />
          <p class="mt-4">Загрузка карточек...</p>
        </v-card>
        <v-card v-else-if="loadError" class="pa-4 text-center">
          <p class="text-error mb-4">{{ loadError }}</p>
          <v-btn color="primary" @click="loadTrainingCards">Попробовать снова</v-btn>
        </v-card>
        <v-card v-else-if="currentCard" class="question-card background-transparent" elevation="0">
          <div class="card-header">
            <div class="chips-group">
              <v-chip
                size="small"
                color="primary"
                prepend-icon="mdi-lightbulb-outline"
                class="category-chip"
              >
                {{ getCategoryName(currentCard) }}
              </v-chip>
              <v-chip
                size="small"
                class="practice-chip"
              >
                {{ getCardType(currentCard) }}
              </v-chip>
            </div>
            <div class="review-info">
              {{ getReviewReason(currentCard) }}
            </div>
          </div>
          <div class="topic-info">
            {{ getTopicInfo(currentCard) }}
          </div>

          <component
            :is="getCardComponent(currentCard)"
            :block="currentCard"
            @answer-submitted="handleAnswer"
            @next="nextCard"
          />
        </v-card>
        <v-card v-else class="pa-4 text-center">
          <p>Нет карточек для тренировки</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCardsStore } from '@/stores/cardsStore'
import { useUserStore } from '@/stores/userStore'
import { useCoursesStore } from '@/stores/coursesStore'
import type { Block } from '@/types'
import { getTrainingCards, submitTrainingAnswer } from '@/services/trainingService'
import TheoryCard from '@/components/cards/TheoryCard.vue'
import PracticeMultipleChoice from '@/components/cards/PracticeMultipleChoice.vue'
import PracticeReflection from '@/components/cards/PracticeReflection.vue'
import PracticeCase from '@/components/cards/PracticeCase.vue'
import PracticeTextInput from '@/components/cards/PracticeTextInput.vue'
import TrainingHeader from '@/components/TrainingHeader.vue'
import { useRouter } from 'vue-router'
import { differenceInDays } from 'date-fns'

const cardsStore = useCardsStore()
const userStore = useUserStore()
const coursesStore = useCoursesStore()
const router = useRouter()

const currentCard = ref<Block | null>(null)
const isLoading = ref(true)
const loadError = ref<string | null>(null)

const loadTrainingCards = async () => {
  isLoading.value = true
  loadError.value = null

  try {
    const response = await getTrainingCards()
    const cards = response.cards

    if (cards.length > 0) {
      currentCard.value = cards[0]
      cardsStore.loadCardsFromBackend(cards)
    } else {
      currentCard.value = null
    }
  } catch (error) {
    console.error('Failed to load training cards:', error)
    loadError.value = 'Не удалось загрузить карточки для тренировки'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadTrainingCards()
})

const getCardComponent = (block: Block) => {
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

const getCategoryName = (block: Block) => {
  const blockId = `${block.type}-${block.order}`
  const repData = cardsStore.spacedRepetitionData.get(blockId)
  if (repData && coursesStore.activeCourse) {
    return coursesStore.activeCourse.category
  }
  return 'Наука'
}

const getCardType = (block: Block) => {
  return block.type === 'theory' ? 'Теория' : 'Практика'
}

const getReviewReason = (block: Block): string => {
  const blockId = `${block.type}-${block.order}`
  const repData = cardsStore.spacedRepetitionData.get(blockId)

  if (repData && repData.lastReview) {
    const daysAgo = differenceInDays(new Date(), repData.lastReview)
    if (daysAgo > 0) {
      return `Вы ошиблись здесь ${daysAgo} ${getDayWord(daysAgo)} назад`
    }
  }
  return 'Пора повторить'
}

const getDayWord = (days: number): string => {
  if (days === 1) return 'день'
  if (days >= 2 && days <= 4) return 'дня'
  return 'дней'
}

const getTopicInfo = (block: Block): string => {
  const blockId = `${block.type}-${block.order}`
  const repData = cardsStore.spacedRepetitionData.get(blockId)

  if (repData && coursesStore.activeCourse) {
    const lessons = coursesStore.getCourseLessons(repData.courseId)
    const lesson = lessons.find(l => l.id === repData.lessonId)
    if (lesson) {
      return `${coursesStore.activeCourse.title} • ${lesson.title}`
    }
    return coursesStore.activeCourse.title
  }
  return 'Основы квантовой физики • Квантовая запутанность'
}

const getBlockId = (block: Block): string => {
  return block.id || `${block.type}-${block.order}`
}

const handleAnswer = async (isCorrect: boolean) => {
  if (currentCard.value) {
    const blockId = getBlockId(currentCard.value)
    const repData = cardsStore.spacedRepetitionData.get(blockId)

    let lessonId = repData?.lessonId
    let courseId = repData?.courseId

    if (!lessonId || !courseId) {
      console.warn('Missing lesson/course context for card, using defaults')
      lessonId = 'lesson_1'
      courseId = coursesStore.activeCourse?.course_id || 'TM-INTER-002'
    }

    try {
      const response = await submitTrainingAnswer({
        block_id: blockId,
        lesson_id: lessonId,
        course_id: courseId,
        is_correct: isCorrect
      })

      cardsStore.updateFromBackendResponse(blockId, lessonId, courseId, response, isCorrect)

      if (isCorrect) {
        userStore.addXP(5)
      }
    } catch (error) {
      console.error('Failed to submit training answer:', error)
      alert('Не удалось сохранить ответ. Проверьте подключение к интернету.')
    }
  }
}

const nextCard = () => {
  userStore.incrementCompletedToday();

  if (cardsStore.reviewQueue.length > 0) {
    currentCard.value = cardsStore.reviewQueue[0]
    cardsStore.reviewQueue = cardsStore.reviewQueue.slice(1)
  } else {
    currentCard.value = null
  }
}
</script>

<style scoped>
.training-container {
  padding-top: 0;
}

.question-card {
  padding: 20px;
  border-radius: var(--border-radius-large);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.chips-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-chip {
  font-weight: 500;
}

.review-info {
  font-size: 12px;
  color: #757575;
  text-align: right;
}

.topic-info {
  font-size: 14px;
  color: #424242;
  margin-bottom: 12px;
  line-height: 1.4;
}

</style>





