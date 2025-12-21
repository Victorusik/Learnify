<template>
  <v-card
    :elevation="3"
    :class="['base-card', $attrs.class]"
    :style="{ borderRadius: '12px' }"
  >
    <slot />
  </v-card>
</template>

<script setup lang="ts">
</script>

<style scoped>
.base-card {
  border-radius: 12px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
}
</style>



