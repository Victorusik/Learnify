// Основные типы курса
export interface Course {
  type: 'course'
  course_id: string
  title: string
  category: string
  subcategory: string
  level: 'Легкий' | 'Средний' | 'Сложный'
  difficulty_score: number
  estimated_duration_weeks: number
  estimated_duration_hours: number
  total_lessons: number
  total_practice_tasks: number
  tags: string[]
  author: string
  creation_date?: string
  last_updated?: string
  status?: string
  language?: string
  target_audience?: string[]
  completion_certificate?: boolean
  short_description: string
  full_description: string
  learning_outcomes: string[]
  prerequisites: string[]
  cover_image_url: string
  promo_video_url?: string
}

// Урок состоит из блоков (карточек)
export interface Lesson {
  id: string
  course_id: string
  order: number
  title: string
  description: string
  blocks: Block[]
}

// Базовый блок (карточка)
export type Block = TheoryBlock | PracticeBlock

// Теоретическая карточка
export interface TheoryBlock {
  type: 'theory'
  order: number
  title: string
  content: string
  visualization_hint: string
}

// Практическая карточка (4 подтипа)
export interface PracticeBlock {
  type: 'practice'
  subtype: 'multiple_choice' | 'reflection' | 'case' | 'text_input'
  order: number
  title: string
  question?: string
  content?: string
  options?: string[]
  hints: string[]
  correct_answer?: string
  explanation?: string
  answer?: string
  sample_answer?: string
}

// Данные для Spaced Repetition
export interface RepetitionData {
  cardId: string
  lessonId: string
  courseId: string
  lastReview: Date | null
  nextReview: Date | null
  interval: number // 1, 7, 16, 35 дней
  easeFactor: number
  needsReview: boolean
  mistakes: number
}

// Достижение
export interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  unlocked: boolean
  unlockedAt?: Date
  progress?: number
  maxProgress?: number
}

// Статистика пользователя
export interface UserStatistics {
  totalLessons: number
  averageAccuracy: number
  daysLearning: number
  totalCardsReviewed: number
}

// Категория курса
export interface Category {
  id: string
  name: string
  icon: string
}





