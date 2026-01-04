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

export interface Lesson {
  id: string
  course_id: string
  order: number
  title: string
  description: string
  blocks: Block[]
}

export type Block = TheoryBlock | PracticeBlock

export interface TheoryBlock {
  id?: string
  type: 'theory'
  order: number
  title: string
  content: string
  visualization_hint: string
  image_url?: string
}

export interface PracticeBlock {
  id?: string
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
  image_url?: string
}

export interface RepetitionData {
  cardId: string
  lessonId: string
  courseId: string
  lastReview: Date | null
  nextReview: Date | null
  interval: number
  easeFactor: number
  needsReview: boolean
  mistakes: number
}

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

export interface UserStatistics {
  totalLessons: number
  averageAccuracy: number
  daysLearning: number
  totalCardsReviewed: number
}

export interface Category {
  id: string
  name: string
  icon: string
}

export interface UserRegister {
  email: string
  password: string
  name: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserProfile {
  id: number
  email: string
  name: string
  is_active: boolean
  level: number
  xp: number
  streak: number
  daily_goal: number
  completed_today: number
  selected_categories: string[]
  notifications: any[]
}

export interface UserUpdate {
  name?: string
  daily_goal?: number
  selected_categories?: string[]
}





