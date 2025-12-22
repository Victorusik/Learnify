<template>
  <BaseCard>
    <v-card-title class="text-h6">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4" v-if="block.question">{{ block.question }}</p>
      <v-radio-group
        v-model="selectedAnswer"
        :disabled="showResult"
      >
        <v-radio
          v-for="(option, index) in block.options"
          :key="index"
          :label="option"
          :value="option"
          class="mb-2"
        />
      </v-radio-group>
      <v-expand-transition>
        <div v-if="showResult" class="mt-4">
          <v-alert
            :type="isCorrect ? 'success' : 'error'"
            :text="isCorrect ? 'Правильно!' : 'Неправильно'"
            class="mb-2"
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
      <v-expand-transition>
        <div v-if="showHints" class="mt-2">
          <v-card variant="outlined" class="pa-3">
            <p class="text-caption font-weight-bold mb-1">Подсказки:</p>
            <ul class="text-caption">
              <li v-for="(hint, index) in block.hints" :key="index">{{ hint }}</li>
            </ul>
          </v-card>
        </div>
      </v-expand-transition>
    </v-card-text>
    <v-card-actions>
      <v-btn
        variant="text"
        @click="showHints = !showHints"
      >
        💡 Подсказка
      </v-btn>
      <v-spacer />
      <v-btn
        v-if="!showResult"
        color="primary"
        :disabled="!selectedAnswer"
        @click="handleAnswer"
      >
        Ответить
      </v-btn>
      <v-btn
        v-else
        color="primary"
        @click="$emit('next')"
      >
        Далее
      </v-btn>
    </v-card-actions>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PracticeBlock } from '@/types'
import BaseCard from './BaseCard.vue'

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




