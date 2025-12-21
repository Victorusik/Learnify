<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-h6">Уровень {{ userStore.level }}</div>
              <div class="text-caption">Стрик: {{ userStore.streak }} дней 🔥</div>
            </div>
            <div class="text-h6">Привет, {{ userStore.name }}!</div>
          </div>
        </v-card>
        <v-card class="pa-4 mb-4">
          <div class="d-flex justify-space-between align-center">
            <span>Сегодня: {{ userStore.completedToday }}/{{ userStore.dailyGoal }} уроков</span>
            <v-btn size="small" variant="text">Изменить цель</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card v-if="currentCard" class="pa-4">
          <div class="d-flex justify-space-between mb-2">
            <v-chip size="small">{{ getCategoryName(currentCard) }}</v-chip>
            <v-chip size="small" variant="outlined">{{ getCardType(currentCard) }}</v-chip>
          </div>
          <div class="text-caption mb-4">{{ getReviewReason(currentCard) }}</div>
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
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <div class="text-caption mb-2">
            Осталось карточек: {{ cardsStore.reviewQueue.length }}
          </div>
          <div class="text-caption">
            Сегодня: {{ cardsStore.todayStats.reviewed }} карточек,
            {{ Math.round(cardsStore.todayStats.accuracy) }}% правильных
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCardsStore } from '@/stores/cardsStore'
import { useUserStore } from '@/stores/userStore'
import type { Block } from '@/types'
import TheoryCard from '@/components/cards/TheoryCard.vue'
import PracticeMultipleChoice from '@/components/cards/PracticeMultipleChoice.vue'
import PracticeReflection from '@/components/cards/PracticeReflection.vue'
import PracticeCase from '@/components/cards/PracticeCase.vue'
import PracticeTextInput from '@/components/cards/PracticeTextInput.vue'

const cardsStore = useCardsStore()
const userStore = useUserStore()

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
  return 'Наука' // TODO: получить из курса
}

const getCardType = (block: Block) => {
  return block.type === 'theory' ? 'Теория' : 'Практика'
}

const getReviewReason = (block: Block) => {
  return 'Пора повторить' // TODO: получить из spaced repetition data
}

const handleAnswer = (isCorrect: boolean) => {
  if (currentCard.value) {
    const blockId = `${currentCard.value.type}-${currentCard.value.order}`
    cardsStore.submitAnswer(blockId, isCorrect, 'lesson_1', 'TM-INTER-002')
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



