<template>
  <div class="practice-multiple-choice">
    <div class="question-section">
      <p class="question-text">{{ block.question }}</p>
    </div>
    <div class="options-section">
      <div
        v-for="(option, index) in block.options"
        :key="index"
        class="option-item"
        :class="{
          'option-item-selected': selectedAnswer === option && !showResult,
          'option-item-correct': showResult && option === block.correct_answer,
          'option-item-incorrect': showResult && selectedAnswer === option && !isCorrect
        }"
        @click="!showResult && (selectedAnswer = option)"
      >
        <div class="option-letter-circle">
          {{ String.fromCharCode(65 + index) }}
        </div>
        <div class="option-text">{{ option }}</div>
      </div>
    </div>
      <div v-if="showResult && block.explanation" class="result-section">
        <v-card
          class="pa-3 box-shadow-2"
        >
          <p class="text-body-2">{{ block.explanation }}</p>
        </v-card>
      </div>

      <div v-if="showHints && block.hints && block.hints.length > 0" class="hints-section">
        <v-card
          class="pa-3 box-shadow-2"
        >
          <p class="text-caption font-weight-bold mb-2">Подсказки:</p>
          <ul class="text-body-2">
            <li v-for="(hint, index) in block.hints" :key="index" class="hint-item">{{ hint }}</li>
          </ul>
        </v-card>
      </div>
    <div class="actions-section">
      <v-btn
        v-if="!showResult"
        color="primary"
        size="large"
        :disabled="!selectedAnswer"
        class="submit-btn"
        @click="handleAnswer"
      >
        Ответить
      </v-btn>
      <v-btn
        v-else
        color="primary"
        size="large"
        class="next-btn"
        @click="$emit('next')"
      >
        Далее
      </v-btn>
      <v-btn
        icon
        variant="text"
        size="small"
        class="hint-btn"
        @click="showHints = !showHints"
      >
        <v-icon>mdi-help-circle-outline</v-icon>
      </v-btn>
      <v-btn
        icon
        variant="text"
        size="small"
        @click="$emit('next')"
      >
        <v-icon>mdi-skip-next</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PracticeBlock } from '@/types'

const props = defineProps<{
  block: PracticeBlock
}>()

const emit = defineEmits<{
  answerSubmitted: [isCorrect: boolean]
  next: []
}>()

const selectedAnswer = ref<string>('')
const showResult = ref(false)
const showHints = ref(false)

const isCorrect = computed(() => {
  return selectedAnswer.value === props.block.correct_answer
})

const handleAnswer = () => {
  showResult.value = true
  emit('answerSubmitted', isCorrect.value)
}
</script>

<style scoped>
.practice-multiple-choice {
  padding: 0;
}

.question-section {
  margin-bottom: 24px;
}

.question-text {
  font-size: var(--question-title-size);
  font-weight: 600;
  line-height: 1.5;
  margin: 0;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px;
  border: 1px solid #e0e0e0;
  border-radius: var(--border-radius-medium);
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.option-item:hover {
  border-color: var(--primary-color);
}

.option-item-selected {
  background-color: rgba(5, 208, 168, 0.1);
  border-color: var(--primary-color);
}

.option-item-correct {
  background-color: rgba(76, 175, 80, 0.1) !important;
  border-color: var(--primary-color) !important;
}

.option-item-incorrect {
  background-color: rgba(244, 67, 54, 0.1) !important;
  border-color: #f44336 !important;
}

.option-letter-circle {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-circle);
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  color: #424242;
  flex-shrink: 0;
}

.option-item-selected .option-letter-circle {
  background-color: var(--primary-color);
  color: white;
}

.option-item-correct .option-letter-circle {
  background-color: var(--primary-color) !important;
  color: white !important;
}

.option-item-incorrect .option-letter-circle {
  background-color: #f44336 !important;
  color: white !important;
}

.option-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  white-space: normal;
}

.result-section {
  border-radius: var(--border-radius-medium);
  margin-bottom: 24px;
}

.hints-section {
  margin-bottom: 24px;
}

.actions-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.submit-btn {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.next-btn {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.hint-btn {
  min-width: 40px;
  width: 40px;
  height: 40px;
}

.hint-item {
list-style-type: none;
}
</style>




