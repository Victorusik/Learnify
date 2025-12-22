<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2 class="text-h5 mb-4">Выберите направление</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="category in categories"
        :key="category.id"
        cols="12"
        md="6"
        class="d-flex"
      >
        <CategoryCard
          class="flex-grow-1"
          :category="category"
          @click="goToCategory(category.id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { mockCategories } from '@/mocks/mockData'
import CategoryCard from '@/components/ui/CategoryCard.vue'

const router = useRouter()
const categories = mockCategories

const goToCategory = (categoryId: string) => {
  router.push(`/learning/category/${categoryId}`)
}
</script>





