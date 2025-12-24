<template>
  <div class="practice-multiple-choice">
    <div class="question-section">
      <p class="question-text">{{ block.question }}</p>
    </div>
    <div class="options-section">
      <v-btn
        v-for="(option, index) in block.options"
        :key="index"
        :variant="selectedAnswer === option ? 'elevated' : 'outlined'"
        :color="selectedAnswer === option ? 'primary' : 'default'"
        :disabled="showResult"
        class="option-btn"
        @click="selectedAnswer = option"
      >
        <span class="option-letter">{{ String.fromCharCode(65 + index) }}:</span>
        <span class="option-text">{{ option }}</span>
      </v-btn>
    </div>
    <v-expand-transition>
      <div v-if="showResult" class="result-section">
        <v-alert
          :type="isCorrect ? 'success' : 'error'"
          :text="isCorrect ? 'Правильно!' : 'Неправильно'"
          class="mb-3"
        />
        <v-card
          v-if="block.explanation"
          variant="outlined"
          class="pa-3"
        >
          <p class="text-body-2">{{ block.explanation }}</p>
        </v-card>
      </div>
    </v-expand-transition>
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
      <div v-else class="next-actions">
        <v-btn
          icon
          variant="text"
          size="small"
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
        <v-btn
          color="primary"
          size="large"
          class="next-btn"
          @click="$emit('next')"
        >
          Далее
        </v-btn>
      </div>
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
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
  color: #000;
  margin: 0;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.option-btn {
  justify-content: flex-start;
  text-transform: none;
  letter-spacing: normal;
  padding: 16px;
  min-height: 56px;
  border-radius: var(--border-radius-medium);
}

.option-letter {
  font-weight: 600;
  margin-right: 8px;
  min-width: 24px;
}

.option-text {
  text-align: left;
  flex: 1;
}

.result-section {
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

.next-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.next-btn {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}
</style>




