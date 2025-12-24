 <template>
  <div class="progress-bar">
    <v-progress-linear
      :model-value="progress"
      :color="color"
      height="8"
      rounded
      class="progress-fill"
    />
    <div class="d-flex justify-space-between mt-1">
      <span class="text-caption" v-if="completedBlocks !== undefined && totalBlocks !== undefined">
        Прогресс: {{ completedBlocks }}/{{ totalBlocks }} карточек
      </span>
      <span class="text-caption" v-else>{{ label }}</span>
      <span class="text-caption">{{ Math.round(progress) }}%</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  progress: number
  color?: string
  completedBlocks?: number
  totalBlocks?: number
}>(), {
  color: 'primary'
})
</script>

<style scoped>
.progress-fill {
  transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
</style>





