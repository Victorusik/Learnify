<template>
  <v-container class="training-container">
    <TrainingHeader @change-goal="router.push('/profile')" />
    <v-row>
      <v-col cols="12">
        <v-card v-if="currentCard" class="question-card background-transparent" elevation="0">
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

onMounted(() => {
  const cards = cardsStore.getCardsForTraining()
  if (cards.length > 0) {
    currentCard.value = cards[0]
    cardsStore.reviewQueue = cards.slice(1)
  }
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

const handleAnswer = (isCorrect: boolean) => {
  if (currentCard.value) {
    const blockId = `${currentCard.value.type}-${currentCard.value.order}`
    const repData = cardsStore.spacedRepetitionData.get(blockId)
    const lessonId = repData?.lessonId || 'lesson_1'
    const courseId = repData?.courseId || 'TM-INTER-002'

    cardsStore.submitAnswer(blockId, isCorrect, lessonId, courseId)
    if (isCorrect) {
      userStore.addXP(5)
    }
  }
}

const nextCard = () => {
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





