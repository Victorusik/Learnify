<template>
  <v-card
    :elevation="3"
    :class="['base-card', $attrs.class]"
    :style="{ borderRadius: 'var(--card-border-radius)' }"
  >
    <slot />
  </v-card>
</template>

<script setup lang="ts">
</script>

<style scoped>
.base-card {
  border-radius: var(--card-border-radius);
  box-shadow: var(--elevation-3);
}
</style>