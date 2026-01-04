export interface RetryOptions {
  maxRetries?: number
  initialDelay?: number
  maxDelay?: number
  backoffMultiplier?: number
  retryableStatuses?: number[]
  retryableErrors?: string[]
}

const DEFAULT_OPTIONS: Required<RetryOptions> = {
  maxRetries: 3,
  initialDelay: 1000,
  maxDelay: 10000,
  backoffMultiplier: 2,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  retryableErrors: ['ECONNABORTED', 'ETIMEDOUT', 'ENOTFOUND', 'ECONNRESET']
}

function calculateDelay(attempt: number, options: Required<RetryOptions>): number {
  const delay = options.initialDelay * Math.pow(options.backoffMultiplier, attempt)
  return Math.min(delay, options.maxDelay)
}

function isRetryable(error: any, options: Required<RetryOptions>): boolean {
  if (error.response) {
    const status = error.response.status
    return options.retryableStatuses.includes(status)
  }

  if (error.code && options.retryableErrors.includes(error.code)) {
    return true
  }

  if (error.message) {
    const message = error.message.toLowerCase()
    return message.includes('timeout') || message.includes('network')
  }

  return false
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const opts = { ...DEFAULT_OPTIONS, ...options }
  let lastError: any

  for (let attempt = 0; attempt <= opts.maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error: any) {
      lastError = error

      if (attempt === opts.maxRetries || !isRetryable(error, opts)) {
        throw error
      }

      const delay = calculateDelay(attempt, opts)
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError
}

