<template>
  <v-bottom-navigation
    :model-value="activeTab"
    @update:model-value="navigate"
    color="primary"
  >
    <v-btn @click="clickAciveTab" value="learning">
      <v-icon>mdi-book-open-variant</v-icon>
      <span>Обучение</span>
    </v-btn>
    <v-btn value="training">
      <v-icon>mdi-brain</v-icon>
      <span>Тренировка</span>
    </v-btn>
    <v-btn value="achievements">
      <v-icon>mdi-trophy</v-icon>
      <span>Достижения</span>
    </v-btn>
    <v-btn value="profile">
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

const clickAciveTab = () => {
  if (route.path === '/learning/categories') {
    router.push('/learning')
  }
}

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


</style>


