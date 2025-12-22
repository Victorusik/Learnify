<template>
  <v-card
    :elevation="3"
    class="category-card"
    :style="{ borderRadius: 'var(--card-border-radius)', cursor: 'pointer' }"
    @click="$emit('click')"
  >
    <v-card-text class="text-center pa-2">
      <div class="text-h2 mb-2">{{ category.icon }}</div>
      <div class="text-h6">{{ category.name }}</div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { Category } from '@/types'

defineProps<{
  category: Category
}>()

defineEmits<{
  click: []
}>()
</script>

<style scoped>
.category-card {
  transition: transform 0.2s;
}

.category-card:hover {
  transform: translateY(-4px);
}
</style>





