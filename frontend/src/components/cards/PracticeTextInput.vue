<template>
  <BaseCard class="box-shadow-2">
    <v-card-title class="question-title">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4" v-if="block.content">{{ block.content }}</p>
      <v-text-field
        v-model="userAnswer"
        label="Ваш ответ"
        :disabled="showSample"
      />
      <div v-if="showHints && block.hints && block.hints.length > 0" class="hints-section">
        <v-card class="pa-3 box-shadow-2">
          <p class="text-caption font-weight-bold mb-2">Подсказки:</p>
          <ul class="text-body-2">
            <li v-for="(hint, index) in block.hints" :key="index" class="hint-item">{{ hint }}</li>
          </ul>
        </v-card>
      </div>
      <v-expand-transition>
        <div v-if="showSample" class="mt-4">
          <v-card variant="outlined" class="pa-3">
            <p class="text-caption font-weight-bold mb-1">Пример ответа:</p>
            <p class="text-body-2">{{ block.sample_answer }}</p>
          </v-card>
        </div>
      </v-expand-transition>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
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
        v-if="!showSample"
        color="primary"
        :disabled="!userAnswer.trim()"
        @click="showSample = true"
      >
        Показать пример
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
import { ref } from 'vue'
import type { PracticeBlock } from '@/types'
import BaseCard from './BaseCard.vue'

defineProps<{
  block: PracticeBlock
}>()

const emit = defineEmits<{
  next: []
}>()

const userAnswer = ref('')
const showHints = ref(false)
const showSample = ref(false)
</script>

<style scoped>
.hints-section {
  margin-bottom: 24px;
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





