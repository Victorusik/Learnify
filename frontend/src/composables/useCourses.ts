import { useCoursesStore } from '@/stores/coursesStore'
import { getCourses, getCourseLessons, enrollCourse as apiEnrollCourse, getEnrolledCourses } from '@/services/coursesService'

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
            store.setCourseLessons(course.course_id, lessons)
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

  const loadEnrolledCourses = async () => {
    // Проверяем авторизацию перед загрузкой
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.log('Пользователь не авторизован, пропускаем загрузку записанных курсов')
      return
    }

    try {
      const enrolledCoursesResponse = await getEnrolledCourses()
      const enrolledCourseIds = enrolledCoursesResponse.map(course => course.course_id)
      store.enrolledCourses = enrolledCourseIds

      // Устанавливаем активный курс, если есть записанные курсы
      if (enrolledCourseIds.length > 0) {
        // Если активный курс не установлен, или текущий активный курс не в списке записанных
        if (!store.activeCourse || !enrolledCourseIds.includes(store.activeCourse.course_id)) {
          // Сначала пытаемся найти курс в уже загруженных курсах
          const firstEnrolledCourse = enrolledCoursesResponse[0]
          let course = store.availableCourses.find(c => c.course_id === firstEnrolledCourse.course_id)

          // Если курс не найден в загруженных, используем данные из ответа API
          if (!course && firstEnrolledCourse) {
            // Преобразуем данные из API в формат Course
            course = {
              ...firstEnrolledCourse,
              category: firstEnrolledCourse.category?.name || 'Без категории'
            } as any
            // Добавляем курс в список доступных, если его там нет
            const existingIndex = store.availableCourses.findIndex(c => c.course_id === firstEnrolledCourse.course_id)
            if (existingIndex === -1) {
              store.availableCourses.push(course)
            }
          }

          if (course) {
            store.activeCourse = course
          }
        }
      }

      console.log('✅ Загружены записанные курсы:', enrolledCourseIds)
    } catch (error: any) {
      // Если ошибка 401, пользователь не авторизован - это нормально
      if (error?.status === 401) {
        console.log('Пользователь не авторизован для загрузки записанных курсов')
        return
      }
      console.error('Failed to load enrolled courses:', error)
      // Не бросаем ошибку, так как это не критично для работы приложения
    }
  }

  const enrollCourse = async (courseId: string) => {
    try {
      await apiEnrollCourse(courseId)
      store.enrollCourse(courseId)
      // Обновляем список записанных курсов с сервера
      await loadEnrolledCourses()
      console.log('✅ Успешно записались на курс:', courseId)
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
    loadEnrolledCourses,
    enrollCourse,
    getCurrentLesson,
    getLessonProgress
  }
}
