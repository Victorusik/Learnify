<template>
  <BaseCard class="box-shadow-2">
    <v-card-title class="question-title">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-2 mb-4">{{ block.content }}</p>

        <v-img
          :src="block.image_url"
          class="border-radius-card mb-4"
          max-height="300"
          cover
        />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="primary"
        @click="$emit('next')"
      >
        Далее
      </v-btn>
    </v-card-actions>
  </BaseCard>
</template>

<script setup lang="ts">
import type { TheoryBlock } from '@/types'
import BaseCard from './BaseCard.vue'

defineProps<{
  block: TheoryBlock
}>()

defineEmits<{
  next: []
}>()
</script>

<style scoped>
.question-title {
  white-space: normal;
}
</style>



