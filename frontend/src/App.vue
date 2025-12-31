<template>
  <v-app>
    <v-main class="app-main">
      <div v-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-4">Загрузка прогресса...</p>
      </div>
      <div v-else-if="loadError" class="error-container">
        <p class="text-error mb-4">{{ loadError }}</p>
        <v-btn color="primary" @click="loadProgress">Попробовать снова</v-btn>
      </div>
      <router-view v-else />
    </v-main>
    <AppNavigation />
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppNavigation from './components/AppNavigation.vue'
import { loadUserProgress } from './services/progressLoader'
import { useCoursesStore } from './stores/coursesStore'

const coursesStore = useCoursesStore()
const isLoading = ref(true)
const loadError = ref<string | null>(null)

const loadProgress = async () => {
  isLoading.value = true
  loadError.value = null

  try {
    const progress = await loadUserProgress()
    coursesStore.loadProgressFromBackend(progress)
    console.log('✅ Progress loaded successfully')
  } catch (error) {
    console.error('Failed to load progress:', error)
    loadError.value = 'Не удалось загрузить прогресс. Проверьте подключение к серверу.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadProgress()
})
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

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  padding: 20px;
  text-align: center;
}

.text-error {
  color: #d32f2f;
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



