<template>
  <v-bottom-navigation
    :model-value="activeTab"
    @update:model-value="navigate"
    class="app-navigation"
    :elevation="0"
    height="65"
  >
    <v-btn value="learning" variant="plain">
      <v-icon>mdi-book-open-variant</v-icon>
      <span>Обучение</span>
    </v-btn>
    <v-btn value="training" variant="plain">
      <v-icon>mdi-brain</v-icon>
      <span>Тренировка</span>
    </v-btn>
    <v-btn value="achievements" variant="plain">
      <v-icon>mdi-trophy</v-icon>
      <span>Достижения</span>
    </v-btn>
    <v-btn value="profile" variant="plain">
      <v-icon>mdi-account</v-icon>
      <span>Профиль</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeTab = computed(() => {
  if (route.path === '/learning/categories') return 'learning'
  if (route.path === '/learning') return 'learning'
  if (route.path === '/main') return 'training'
  if (route.path === '/achievements') return 'achievements'
  if (route.path === '/profile') return 'profile'
  return 'training'
})

const navigate = (value: string) => {
  switch (value) {
    case 'learning':
      router.push('/learning')
      break
    case 'training':
      router.push('/main')
      break
    case 'achievements':
      router.push('/achievements')
      break
    case 'profile':
      router.push('/profile')
      break
  }
}
</script>

<style scoped>
.app-navigation {
  background-color: white !important;
  border-top: 1px solid #d7e0de;
  box-shadow: none !important;
}

.app-navigation :deep(.v-bottom-navigation__content) {
  gap: 5px;
}

.app-navigation :deep(.v-btn) {
  color: #9e9e9e !important;
  background-color: transparent !important;
  background: transparent !important;
}

.app-navigation :deep(.v-btn--active) {
  background-color: transparent !important;
  background: transparent !important;
  color: var(--primary-color) !important;
}

.app-navigation :deep(.v-btn--active .v-icon),
.app-navigation :deep(.v-btn--active span) {
  color: var(--primary-color) !important;
}

.app-navigation :deep(.v-btn:hover),
.app-navigation :deep(.v-btn:focus),
.app-navigation :deep(.v-btn:focus-visible) {
  background-color: transparent !important;
  background: transparent !important;
}

@media (min-width: 600px) {
  .v-bottom-navigation__content {
    max-width: var(--app-max-width);
    margin: 0 auto;
  }
}
</style>


