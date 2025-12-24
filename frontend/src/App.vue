<template>
  <v-app>
    <v-main class="app-main">
      <router-view />
    </v-main>
    <AppNavigation />
  </v-app>
</template>

<script setup lang="ts">
import AppNavigation from './components/AppNavigation.vue'
</script>

<style>
#app {
  background-color: var(--background-color-1);
}

.v-application {
  background-color: transparent;
  font-family: var(--font-family) !important;
}

.v-application,
.v-application * {
  font-family: var(--font-family) !important;
  letter-spacing: normal !important;
}

.v-btn {
  text-transform: none !important;
}

.app-main {
  background-color: var(--background-color-1);
}

@media (min-width: 600px) {
  .v-application {
    max-width: var(--app-max-width);
    margin: 0 auto;
  }

  .v-main {
    max-width: var(--app-max-width);
  }
}
</style>



