<template>
  <BaseCard>
    <v-card-title class="text-h6">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4" v-if="block.content">{{ block.content }}</p>
      <v-text-field
        v-model="userAnswer"
        label="Ваш ответ"
        :disabled="showSample"
      />
      <v-expand-transition>
        <div v-if="showHints" class="mt-2 mb-2">
          <v-card variant="outlined" class="pa-3">
            <p class="text-caption font-weight-bold mb-1">Подсказки:</p>
            <ul class="text-caption">
              <li v-for="(hint, index) in block.hints" :key="index">{{ hint }}</li>
            </ul>
          </v-card>
        </div>
      </v-expand-transition>
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
      <v-btn
        variant="text"
        @click="showHints = !showHints"
      >
        💡 Подсказка
      </v-btn>
      <v-spacer />
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



