<template>
  <div class="activity-calendar">
    <div class="calendar-header">
      <div
        v-for="day in weekDays"
        :key="day"
        class="day-header"
      >
        {{ day }}
      </div>
    </div>
    <div class="calendar-grid">
      <div
        v-for="(day, index) in calendarDays"
        :key="index"
        class="calendar-day"
        :class="{ 'active': day.active, 'current': day.isCurrent }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { subDays, format, isSameDay } from 'date-fns'

interface Day {
  active: boolean
  isCurrent: boolean
}

const props = withDefaults(defineProps<{
  activityData?: Map<string, boolean>
}>(), {
  activityData: () => new Map<string, boolean>()
})

const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const calendarDays = computed<Day[]>(() => {
  const days: Day[] = []
  const today = new Date()

  // Генерируем 28 дней (4 недели) назад от сегодня
  for (let i = 27; i >= 0; i--) {
    const date = subDays(today, i)
    const dateKey = format(date, 'yyyy-MM-dd')
    const isActive = props.activityData.get(dateKey) || false
    const isCurrent = isSameDay(date, today)

    days.push({
      active: isActive,
      isCurrent
    })
  }

  return days
})
</script>

<style scoped>
.activity-calendar {
  width: 100%;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.day-header {
  font-size: 12px;
  color: #757575;
  text-align: center;
  font-weight: 500;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;
  background-color: #f5f5f5;
  border-radius: var(--border-radius-small);
  transition: background-color 0.2s;
}

.calendar-day.active {
  background-color: var(--secondary-color);
}

.calendar-day.current {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
  box-sizing: border-box;
}
</style>

