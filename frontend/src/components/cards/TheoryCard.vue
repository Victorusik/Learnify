<template>
  <BaseCard>
    <v-card-title class="text-h6">{{ block.title }}</v-card-title>
    <v-card-text>
      <p class="text-body-1 mb-4">{{ block.content }}</p>
      <v-card
        v-if="block.visualization_hint"
        variant="outlined"
        class="pa-4 mb-4"
        style="background-color: #f5f5f5;"
      >
        <p class="text-caption text-medium-emphasis">
          {{ block.visualization_hint }}
        </p>
      </v-card>
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





