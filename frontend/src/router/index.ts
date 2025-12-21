import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/main'
  },
  {
    path: '/learning',
    name: 'Learning',
    component: () => import('@/views/learning/LearningView.vue')
  },
  {
    path: '/learning/categories',
    name: 'Categories',
    component: () => import('@/views/learning/CategoriesView.vue')
  },
  {
    path: '/learning/category/:id',
    name: 'CategoryCourses',
    component: () => import('@/views/learning/CategoryCoursesView.vue')
  },
  {
    path: '/learning/course/:id',
    name: 'CourseDetails',
    component: () => import('@/views/learning/CourseDetailsView.vue')
  },
  {
    path: '/learning/course/:courseId/lesson/:lessonId',
    name: 'Lesson',
    component: () => import('@/views/learning/LessonView.vue')
  },
  {
    path: '/main',
    name: 'Training',
    component: () => import('@/views/TrainingView.vue')
  },
  {
    path: '/achievements',
    name: 'Achievements',
    component: () => import('@/views/AchievementsView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router



