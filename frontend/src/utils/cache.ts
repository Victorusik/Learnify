/**
 * Простой кэш для хранения данных в localStorage
 */

interface CacheEntry<T> {
  data: T
  timestamp: number
  ttl: number
}

export class Cache {
  private prefix: string

  constructor(prefix: string = 'learnify_cache') {
    this.prefix = prefix
  }

  /**
   * Сохраняет данные в кэш
   */
  set<T>(key: string, data: T, ttl: number = 3600000): void {
    try {
      const entry: CacheEntry<T> = {
        data,
        timestamp: Date.now(),
        ttl
      }
      localStorage.setItem(`${this.prefix}_${key}`, JSON.stringify(entry))
    } catch (error) {
      console.warn('Failed to save to cache:', error)
    }
  }

  /**
   * Получает данные из кэша
   */
  get<T>(key: string): T | null {
    try {
      const item = localStorage.getItem(`${this.prefix}_${key}`)
      if (!item) return null

      const entry: CacheEntry<T> = JSON.parse(item)
      const now = Date.now()

      // Проверяем, не истек ли срок действия
      if (now - entry.timestamp > entry.ttl) {
        this.delete(key)
        return null
      }

      return entry.data
    } catch (error) {
      console.warn('Failed to read from cache:', error)
      return null
    }
  }

  /**
   * Удаляет запись из кэша
   */
  delete(key: string): void {
    try {
      localStorage.removeItem(`${this.prefix}_${key}`)
    } catch (error) {
      console.warn('Failed to delete from cache:', error)
    }
  }

  /**
   * Очищает весь кэш
   */
  clear(): void {
    try {
      const keys = Object.keys(localStorage)
      keys.forEach(key => {
        if (key.startsWith(`${this.prefix}_`)) {
          localStorage.removeItem(key)
        }
      })
    } catch (error) {
      console.warn('Failed to clear cache:', error)
    }
  }
}

export const cache = new Cache()

