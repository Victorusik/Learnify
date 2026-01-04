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
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import AppNavigation from './components/AppNavigation.vue'
import { loadUserProgress } from './services/progressLoader'
import { useCoursesStore } from './stores/coursesStore'
import { useUserStore } from './stores/userStore'
import { getAccessToken } from './services/authService'

const coursesStore = useCoursesStore()
const userStore = useUserStore()
const route = useRoute()
const isLoading = ref(true)
const loadError = ref<string | null>(null)

const isPublicRoute = () => {
  const publicRoutes = ['/login', '/register']
  return publicRoutes.includes(route.path)
}

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

const initializeApp = async () => {
  if (isPublicRoute()) {
    isLoading.value = false
    return
  }

  await nextTick()

  const hasToken = getAccessToken() !== null

  if (hasToken) {
    try {
      await userStore.fetchProfile()
    } catch (error: any) {
      console.error('Ошибка загрузки профиля:', error)
      if (error?.response?.status === 401) {
        userStore.logout()
        isLoading.value = false
        return
      }
      loadError.value = 'Не удалось загрузить профиль пользователя.'
      isLoading.value = false
      return
    }
  } else {
    isLoading.value = false
    return
  }

  if (userStore.user) {
    await loadProgress()
  } else {
    isLoading.value = false
  }
}

onMounted(() => {
  initializeApp()
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



