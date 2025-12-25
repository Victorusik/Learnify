<template>
  <BaseCard class="box-shadow-2">
    <v-card-title class="question-title">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4" v-if="block.content">{{ block.content }}</p>
      <v-expand-transition>
        <div v-if="showHints" class="mb-4">
          <v-card variant="outlined" class="pa-3">
            <p class="text-caption font-weight-bold mb-1">Подсказки:</p>
            <ul class="text-caption">
              <li v-for="(hint, index) in block.hints" :key="index">{{ hint }}</li>
            </ul>
          </v-card>
        </div>
      </v-expand-transition>
      <v-expand-transition>
        <div v-if="showAnswer" class="mt-4">
          <v-card
            variant="outlined"
            class="pa-3"
            style="background-color: #e8f5e9;"
          >
            <p class="text-caption font-weight-bold mb-1">Решение:</p>
            <p class="text-body-2">{{ block.answer }}</p>
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
        v-if="!showAnswer"
        color="primary"
        @click="showAnswer = true"
      >
        Показать решение
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

const showHints = ref(false)
const showAnswer = ref(false)
</script>




