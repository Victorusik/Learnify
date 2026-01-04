import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Course, Lesson } from '@/types'
import type { UserProgressResponse } from '@/services/progressService'
import type { LessonListItem } from '@/services/coursesService'

export const useCoursesStore = defineStore('courses', () => {
  const activeCourse = ref<Course | null>(null)
  const availableCourses = ref<Course[]>([])
  const enrolledCourses = ref<string[]>([])
  const completedLessons = ref<string[]>([])
  const currentLesson = ref<Lesson | null>(null)
  const lessonsProgress = ref<Map<string, number>>(new Map())

  const courseLessons = ref<Map<string, LessonListItem[]>>(new Map())

  const getCourseLessons = (courseId: string): LessonListItem[] => {
    return courseLessons.value.get(courseId) || []
  }

  const setCourseLessons = (courseId: string, lessons: LessonListItem[]) => {
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

    // Calculate progress based on completed lessons
    // We use lessonsProgress which tracks completed blocks per lesson
    let totalLessonsCompleted = 0
    let totalLessons = lessons.length

    lessons.forEach(lesson => {
      // If lesson is marked as completed, count it
      if (completedLessons.value.includes(lesson.id)) {
        totalLessonsCompleted += 1
      }
    })

    return totalLessons > 0 ? (totalLessonsCompleted / totalLessons) * 100 : 0
  }

  const getCurrentLesson = (): LessonListItem | null => {
    if (!activeCourse.value) return null

    const lessons = getCourseLessons(activeCourse.value.course_id)
    if (lessons.length === 0) return null

    // Return the first incomplete lesson
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

  const loadProgressFromBackend = (progress: UserProgressResponse) => {
    const lessonsProgressMap = new Map<string, number>()
    const completedLessonsSet = new Set<string>()

    progress.progress.forEach(item => {
      const current = lessonsProgressMap.get(item.lesson_id) || 0
      lessonsProgressMap.set(item.lesson_id, current + 1)
    })

    lessonsProgress.value = lessonsProgressMap
    completedLessons.value = Array.from(completedLessonsSet)
  }

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

