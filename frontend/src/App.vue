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

<style>


.v-application {
  background-color: var(--background-color-1);
  font-family: var(--font-family) !important;
}

.v-application,
.v-application * {
  font-family: var(--font-family) !important;
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



