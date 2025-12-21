<template>
  <v-app>
    <v-main>
      <router-view />
      <AppNavigation />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import AppNavigation from './components/AppNavigation.vue'
</script>

<style scoped>
</style>


