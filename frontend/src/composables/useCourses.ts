import { useCoursesStore } from '@/stores/coursesStore'
import { mockCourseData, mockAdditionalCourses } from '@/mocks/mockData'

export function useCourses() {
  const store = useCoursesStore()

  const initializeCourses = () => {
    if (store.availableCourses.length === 0) {
      store.availableCourses.push(mockCourseData.course, ...mockAdditionalCourses)
      store.setCourseLessons('TM-INTER-002', mockCourseData.lessons)

      console.log('📚 Загружено курсов:', store.availableCourses.length)
      console.log('📋 Доступные курсы:', store.availableCourses)
      console.log('📖 Уроки для TM-INTER-002:', store.getCourseLessons('TM-INTER-002'))
    } else {
      console.log('✅ Данные уже загружены ранее')
    }
  }

  const enrollCourse = (courseId: string) => {
    store.enrollCourse(courseId)
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





