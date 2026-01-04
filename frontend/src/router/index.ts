import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { getAccessToken } from '@/services/authService'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/main'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresAuth: false }
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

// Navigation guard для защиты приватных роутов
router.beforeEach((to, from, next) => {
  // Проверяем токен напрямую из localStorage (более надежно, чем через computed)
  const hasToken = getAccessToken() !== null

  // Публичные роуты (логин и регистрация)
  const publicRoutes = ['/login', '/register']
  const isPublicRoute = publicRoutes.includes(to.path)

  // Если пользователь авторизован и пытается зайти на страницу логина/регистрации
  if (hasToken && isPublicRoute) {
    next('/main')
    return
  }

  // Если пользователь не авторизован и пытается зайти на приватную страницу
  if (!hasToken && !isPublicRoute) {
    next('/login')
    return
  }

  next()
})

export default router





