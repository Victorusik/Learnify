/**
 * Реализация паттерна Circuit Breaker
 */

export const CircuitState = {
  CLOSED: 'CLOSED',      // Нормальная работа
  OPEN: 'OPEN',          // Разомкнут (ошибки)
  HALF_OPEN: 'HALF_OPEN' // Тестирование восстановления
} as const

export type CircuitState = typeof CircuitState[keyof typeof CircuitState]

export interface CircuitBreakerOptions {
  failureThreshold?: number      // Порог ошибок для открытия
  successThreshold?: number       // Порог успехов для закрытия
  timeout?: number                // Таймаут в OPEN состоянии (мс)
  resetTimeout?: number           // Время до попытки восстановления (мс)
}

const DEFAULT_OPTIONS: Required<CircuitBreakerOptions> = {
  failureThreshold: 5,
  successThreshold: 2,
  timeout: 60000,  // 1 минута
  resetTimeout: 30000  // 30 секунд
}

export class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED
  private failureCount = 0
  private successCount = 0
  private lastFailureTime: number | null = null
  private options: Required<CircuitBreakerOptions>

  constructor(options: CircuitBreakerOptions = {}) {
    this.options = { ...DEFAULT_OPTIONS, ...options }
  }

  /**
   * Выполняет функцию через circuit breaker
   */
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    this.checkState()

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  /**
   * Проверяет текущее состояние и обновляет его при необходимости
   */
  private checkState(): void {
    const now = Date.now()

    if (this.state === CircuitState.OPEN) {
      if (this.lastFailureTime && (now - this.lastFailureTime) >= this.options.resetTimeout) {
        this.state = CircuitState.HALF_OPEN
        this.successCount = 0
      } else {
        throw new Error('Circuit breaker is OPEN')
      }
    }
  }

  /**
   * Обработка успешного выполнения
   */
  private onSuccess(): void {
    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++
      if (this.successCount >= this.options.successThreshold) {
        this.state = CircuitState.CLOSED
        this.failureCount = 0
        this.successCount = 0
      }
    } else if (this.state === CircuitState.CLOSED) {
      this.failureCount = 0
    }
  }

  /**
   * Обработка ошибки
   */
  private onFailure(): void {
    this.failureCount++
    this.lastFailureTime = Date.now()

    if (this.failureCount >= this.options.failureThreshold) {
      this.state = CircuitState.OPEN
    } else if (this.state === CircuitState.HALF_OPEN) {
      this.state = CircuitState.OPEN
      this.successCount = 0
    }
  }

  /**
   * Получить текущее состояние
   */
  getState(): CircuitState {
    return this.state
  }

  /**
   * Сбросить состояние
   */
  reset(): void {
    this.state = CircuitState.CLOSED
    this.failureCount = 0
    this.successCount = 0
    this.lastFailureTime = null
  }
}

