import { useCoursesStore } from '@/stores/coursesStore'
import { getCourses, getCourseLessons, enrollCourse as apiEnrollCourse } from '@/services/coursesService'

export function useCourses() {
  const store = useCoursesStore()

  const initializeCourses = async () => {
    if (store.availableCourses.length === 0) {
      try {
        const coursesResponse = await getCourses()
        const courses = coursesResponse.map(course => ({
          ...course,
          category: course.category?.name || 'Без категории'
        }))
        store.availableCourses = courses

        for (const course of courses) {
          try {
            const lessons = await getCourseLessons(course.course_id)
            // store.setCourseLessons(course.course_id, lessons)
          } catch (error) {
            console.error(`Failed to load lessons for course ${course.course_id}:`, error)
          }
        }

        console.log('📚 Загружено курсов с бэкенда:', store.availableCourses.length)
        console.log('📋 Доступные курсы:', store.availableCourses)
      } catch (error) {
        console.error('Failed to load courses from backend:', error)
        throw error
      }
    } else {
      console.log('✅ Данные уже загружены ранее')
    }
  }

  const enrollCourse = async (courseId: string) => {
    try {
      await apiEnrollCourse(courseId)
      store.enrollCourse(courseId)
    } catch (error) {
      console.error('Failed to enroll in course:', error)
      throw error
    }
  }

  const getCurrentLesson = () => {
    return store.getCurrentLesson()
  }

  const getLessonProgress = (lessonId: string) => {
    return store.getLessonProgress(lessonId)
  }

  return {
    initializeCourses,
    enrollCourse,
    getCurrentLesson,
    getLessonProgress
  }
}





