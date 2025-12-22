<template>
  <BaseCard>
    <v-card-title class="text-h6">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4">{{ block.content }}</p>

        <v-img
          src="https://img.freepik.com/premium-photo/majestic-lion-wearing-elegant-crown-against-dark-background_626475-6901.jpg?semt=ais_hybrid&w=740"
          class="mb-4"
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





