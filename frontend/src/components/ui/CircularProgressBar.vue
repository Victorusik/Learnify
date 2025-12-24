<template>
  <div class="circular-progress-bar">
    <svg
      :width="size"
      :height="size"
      class="progress-svg"
    >
      <circle
        cx="50%"
        cy="50%"
        :r="radius"
        class="progress-bg"
        :stroke-width="strokeWidth"
      />
      <circle
        cx="50%"
        cy="50%"
        :r="radius"
        class="progress-fill"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
      />
    </svg>
    <div class="progress-text">
      <span class="progress-value">{{ Math.round(progress) }}%</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  progress: number
  size?: number
  strokeWidth?: number
}>(), {
  size: 80,
  strokeWidth: 8
})

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const dashOffset = computed(() => circumference.value - (props.progress / 100) * circumference.value)
</script>

<style scoped>
.circular-progress-bar {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.progress-svg {
  transform: rotate(-90deg);
}

.progress-bg {
  fill: none;
  stroke: #e0e0e0;
}

.progress-fill {
  fill: none;
  stroke: var(--primary-color);
  stroke-linecap: round;
  transition: stroke-dashoffset 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-value {
  font-size: 20px;
  font-weight: 600;
  color: #424242;
}
</style>

