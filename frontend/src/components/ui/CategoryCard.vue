<template>
  <v-card
    class="category-card box-shadow-2"
    @click="$emit('click')"
  >
    <v-card-text class="text-left pa-3">
      <div class="category-icon mb-2">{{ category.icon }}</div>
      <div class="category-name">{{ category.name }}</div>
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
  border-radius: var(--card-border-radius);
   cursor: 'pointer';
}

.category-icon {
  font-size: 32px;
  line-height: 1;
}

.category-name {
  font-size: 16px;
  font-weight: 500;
}
</style>





