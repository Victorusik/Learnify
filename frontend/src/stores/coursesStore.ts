import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Course, Lesson } from '@/types'
import type { UserProgressResponse } from '@/services/progressService'

export const useCoursesStore = defineStore('courses', () => {
  const activeCourse = ref<Course | null>(null)
  const availableCourses = ref<Course[]>([])
  const enrolledCourses = ref<string[]>([])
  const completedLessons = ref<string[]>([])
  const currentLesson = ref<Lesson | null>(null)
  const lessonsProgress = ref<Map<string, number>>(new Map())

  const courseLessons = ref<Map<string, Lesson[]>>(new Map())

  const getCourseLessons = (courseId: string): Lesson[] => {
    return courseLessons.value.get(courseId) || []
  }

  const setCourseLessons = (courseId: string, lessons: Lesson[]) => {
    courseLessons.value.set(courseId, lessons)
  }

  const getLessonBlocks = (lessonId: string) => {
    if (!currentLesson.value || currentLesson.value.id !== lessonId) {
      return []
    }
    return currentLesson.value.blocks
  }

  const enrollCourse = (courseId: string) => {
    if (!enrolledCourses.value.includes(courseId)) {
      enrolledCourses.value.push(courseId)
    }
    const course = availableCourses.value.find(c => c.course_id === courseId)
    if (course) {
      activeCourse.value = course
    }
  }

  const markBlockCompleted = (lessonId: string, /* blockOrder: number */) => {
    const current = lessonsProgress.value.get(lessonId) || 0
    // Создаем новую Map для реактивности
    const newMap = new Map(lessonsProgress.value)
    newMap.set(lessonId, current + 1)
    lessonsProgress.value = newMap
  }

  const getLessonProgress = (lessonId: string): number => {
    if (!currentLesson.value || currentLesson.value.id !== lessonId) {
      return 0
    }
    const completed = lessonsProgress.value.get(lessonId) || 0
    const total = currentLesson.value.blocks.length
    return total > 0 ? (completed / total) * 100 : 0
  }

  const getCourseProgress = (courseId: string): number => {
    const course = availableCourses.value.find(c => c.course_id === courseId)
    if (!course) return 0

    const lessons = getCourseLessons(courseId)
    if (lessons.length === 0) return 0

    let totalBlocks = 0
    let completedBlocks = 0

    lessons.forEach(lesson => {
      totalBlocks += lesson.blocks.length
      completedBlocks += lessonsProgress.value.get(lesson.id) || 0
    })

    return totalBlocks > 0 ? (completedBlocks / totalBlocks) * 100 : 0
  }

  const getCurrentLesson = (): Lesson | null => {
    if (!activeCourse.value) return null

    const lessons = getCourseLessons(activeCourse.value.course_id)
    for (const lesson of lessons) {
      if (!completedLessons.value.includes(lesson.id)) {
        return lesson
      }
    }
    return null
  }

  const completeLesson = (lessonId: string) => {
    if (!completedLessons.value.includes(lessonId)) {
      completedLessons.value.push(lessonId)
    }
  }

  /**
   * Загружает прогресс с бэкенда и синхронизирует с локальным состоянием
   */
  const loadProgressFromBackend = (progress: UserProgressResponse) => {
    const lessonsProgressMap = new Map<string, number>()
    const completedLessonsSet = new Set<string>()

    // Группируем блоки по урокам
    progress.progress.forEach(item => {
      const current = lessonsProgressMap.get(item.lesson_id) || 0
      lessonsProgressMap.set(item.lesson_id, current + 1)
    })

    // Обновляем реактивное состояние
    lessonsProgress.value = lessonsProgressMap
    completedLessons.value = Array.from(completedLessonsSet)
  }

  /**
   * Синхронизирует завершенные уроки
   */
  const syncCompletedLessons = (lessons: string[]) => {
    completedLessons.value = lessons
  }

  return {
    activeCourse,
    availableCourses,
    enrolledCourses,
    completedLessons,
    currentLesson,
    lessonsProgress,
    getCourseLessons,
    setCourseLessons,
    getLessonBlocks,
    enrollCourse,
    markBlockCompleted,
    getLessonProgress,
    getCourseProgress,
    getCurrentLesson,
    completeLesson,
    loadProgressFromBackend,
    syncCompletedLessons
  }
})

