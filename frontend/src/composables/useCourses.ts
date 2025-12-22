import { useCoursesStore } from '@/stores/coursesStore'
import { mockCourseData, mockAdditionalCourses } from '@/mocks/mockData'

export function useCourses() {
  const store = useCoursesStore()

  const initializeCourses = () => {
    if (store.availableCourses.length === 0) {
      store.availableCourses.push(mockCourseData.course, ...mockAdditionalCourses)
      store.setCourseLessons('TM-INTER-002', mockCourseData.lessons)
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




