<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="text-h5 mb-2">{{ userStore.name }} (Уровень {{ userStore.level }})</div>
          <ProgressBar
            :progress="userStore.xpProgress"
            :label="`До следующего уровня: ${userStore.xpToNextLevel} XP`"
          />
          <div class="text-caption mt-2">Всего опыта: {{ userStore.xp }} XP</div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="text-h6 mb-2">Стрики</div>
          <div class="text-body-1 mb-2">Текущая серия: {{ userStore.streak }} дней 🔥</div>
          <div class="text-caption">Рекорд: 21 день</div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <div class="text-h6 mb-4">Активность</div>
          <div v-for="day in achievementsStore.weeklyActivity" :key="day.day" class="mb-2">
            <div class="d-flex align-center">
              <span class="mr-2" style="width: 30px;">{{ day.day }}:</span>
              <v-progress-linear
                :model-value="(day.lessons / 20) * 100"
                height="20"
                rounded
                class="flex-grow-1"
              />
              <span class="ml-2">{{ day.lessons }} уроков</span>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <div class="text-h6 mb-4">Награды</div>
          <div class="mb-4">
            <div class="text-subtitle-2 mb-2">Полученные ({{ unlockedCount }}):</div>
            <div class="d-flex flex-wrap gap-2">
              <v-chip
                v-for="achievement in unlockedAchievements"
                :key="achievement.id"
                color="success"
                size="large"
              >
                {{ achievement.icon }} {{ achievement.title }}
              </v-chip>
            </div>
          </div>
          <div>
            <div class="text-subtitle-2 mb-2">В процессе ({{ inProgressCount }}):</div>
            <div class="d-flex flex-wrap gap-2">
              <v-chip
                v-for="achievement in inProgressAchievements"
                :key="achievement.id"
                variant="outlined"
                size="large"
              >
                {{ achievement.icon }} {{ achievement.title }}
                <span v-if="achievement.progress !== undefined">
                  ({{ achievement.progress }}/{{ achievement.maxProgress }})
                </span>
              </v-chip>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useAchievementsStore } from '@/stores/achievementsStore'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import { mockAchievements } from '@/mocks/mockData'

const userStore = useUserStore()
const achievementsStore = useAchievementsStore()

const unlockedAchievements = computed(() => {
  return mockAchievements.filter(a => a.unlocked)
})

const inProgressAchievements = computed(() => {
  return mockAchievements.filter(a => !a.unlocked && a.progress !== undefined)
})

const unlockedCount = computed(() => unlockedAchievements.value.length)
const inProgressCount = computed(() => inProgressAchievements.value.length)
</script>




