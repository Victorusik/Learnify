import { defineStore } from 'pinia'
import { ref } from 'vue'
import { addDays, isBefore } from 'date-fns'
import type { Block, RepetitionData } from '@/types'
import type { TrainingSubmitResponse } from '@/services/trainingService'

export const useCardsStore = defineStore('cards', () => {
  const allBlocks = ref<Block[]>([])

  const initializeBlocks = (blocks: Block[]) => {
    allBlocks.value = blocks
  }
  const reviewQueue = ref<Block[]>([])
  const spacedRepetitionData = ref<Map<string, RepetitionData>>(new Map())

  const todayStats = ref({
    reviewed: 0,
    correct: 0,
    accuracy: 0
  })

  const calculateNextReview = (cardId: string, isCorrect: boolean): Date => {
    const data = spacedRepetitionData.value.get(cardId)
    if (!data) {
      return addDays(new Date(), 1)
    }

    let newInterval = data.interval
    let newEaseFactor = data.easeFactor || 2.5

    if (isCorrect) {
      newInterval = Math.floor(newInterval * newEaseFactor)
      newEaseFactor = Math.min(newEaseFactor + 0.1, 2.5)
    } else {
      newInterval = Math.max(1, Math.floor(newInterval / 2))
      newEaseFactor = Math.max(1.3, newEaseFactor - 0.2)
    }

    const intervals = [1, 7, 16, 35]
    const closestInterval = intervals.reduce((prev, curr) => {
      return Math.abs(curr - newInterval) < Math.abs(prev - newInterval) ? curr : prev
    })
    newInterval = closestInterval

    return addDays(new Date(), newInterval)
  }

  const getCardsForTraining = (): Block[] => {
    const now = new Date()
    const cards: Block[] = []

    const needsReview = allBlocks.value.filter(block => {
      const data = spacedRepetitionData.value.get(`${block.type}-${block.order}`)
      return data?.needsReview === true
    })

    const dueForReview = allBlocks.value.filter(block => {
      const data = spacedRepetitionData.value.get(`${block.type}-${block.order}`)
      if (!data || data.needsReview) return false
      return data.nextReview && isBefore(data.nextReview, now)
    })

    const newCards = allBlocks.value.filter(block => {
      return !spacedRepetitionData.value.has(`${block.type}-${block.order}`)
    }).slice(0, 2)

    cards.push(...needsReview.slice(0, 5))
    cards.push(...dueForReview.slice(0, 5))
    cards.push(...newCards)

    return cards.slice(0, 10)
  }

  const submitAnswer = (blockId: string, isCorrect: boolean, lessonId: string, courseId: string) => {
    const data = spacedRepetitionData.value.get(blockId) || {
      cardId: blockId,
      lessonId,
      courseId,
      lastReview: null,
      nextReview: null,
      interval: 1,
      easeFactor: 2.5,
      needsReview: false,
      mistakes: 0
    }

    data.lastReview = new Date()
    data.nextReview = calculateNextReview(blockId, isCorrect)
    data.needsReview = !isCorrect
    if (!isCorrect) {
      data.mistakes += 1
    } else {
      data.needsReview = false
    }

    spacedRepetitionData.value.set(blockId, data)

    todayStats.value.reviewed += 1
    if (isCorrect) {
      todayStats.value.correct += 1
    }
    todayStats.value.accuracy = todayStats.value.reviewed > 0
      ? (todayStats.value.correct / todayStats.value.reviewed) * 100
      : 0
  }

  const markCardAsReviewed = (blockId: string) => {
    const data = spacedRepetitionData.value.get(blockId)
    if (data) {
      data.needsReview = false
    }
  }

  const updateFromBackendResponse = (
    blockId: string,
    lessonId: string,
    courseId: string,
    response: TrainingSubmitResponse,
    isCorrect: boolean
  ) => {
    const data: RepetitionData = {
      cardId: blockId,
      lessonId,
      courseId,
      lastReview: new Date(),
      nextReview: new Date(response.next_review),
      interval: response.interval,
      easeFactor: 2.5,
      needsReview: response.needs_review,
      mistakes: 0
    }

    const existing = spacedRepetitionData.value.get(blockId)
    if (existing) {
      data.mistakes = existing.mistakes + (isCorrect ? 0 : 1)
    } else {
      data.mistakes = isCorrect ? 0 : 1
    }

    spacedRepetitionData.value.set(blockId, data)

    todayStats.value.reviewed += 1
    if (isCorrect) {
      todayStats.value.correct += 1
    }
    todayStats.value.accuracy = todayStats.value.reviewed > 0
      ? (todayStats.value.correct / todayStats.value.reviewed) * 100
      : 0
  }

  const loadCardsFromBackend = (cards: Block[]) => {
    allBlocks.value = cards
    reviewQueue.value = cards.slice(1)
  }

  return {
    allBlocks,
    reviewQueue,
    spacedRepetitionData,
    todayStats,
    getCardsForTraining,
    submitAnswer,
    markCardAsReviewed,
    calculateNextReview,
    initializeBlocks,
    updateFromBackendResponse,
    loadCardsFromBackend
  }
})

