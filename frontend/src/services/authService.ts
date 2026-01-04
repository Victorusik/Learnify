import apiClient from './api'
import type { UserRegister, UserLogin, TokenResponse, UserProfile } from '@/types'

const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * Сохраняет токены в localStorage
 */
function saveTokens(accessToken: string, refreshToken: string): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
}

/**
 * Удаляет токены из localStorage
 */
function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/**
 * Получает access token из localStorage
 */
export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

/**
 * Получает refresh token из localStorage
 */
function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

/**
 * Регистрация нового пользователя
 */
export async function register(email: string, password: string, name: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/auth/register', {
    email,
    password,
    name
  } as UserRegister)

  const { access_token, refresh_token } = response.data
  saveTokens(access_token, refresh_token)

  return response.data
}

/**
 * Авторизация пользователя
 */
export async function login(email: string, password: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/auth/login', {
    email,
    password
  } as UserLogin)

  const { access_token, refresh_token } = response.data
  saveTokens(access_token, refresh_token)

  return response.data
}

/**
 * Выход из системы
 */
export function logout(): void {
  clearTokens()
}

/**
 * Обновление access token через refresh token
 */
export async function refreshToken(): Promise<TokenResponse | null> {
  const refreshToken = getRefreshToken()

  if (!refreshToken) {
    return null
  }

  try {
    const response = await apiClient.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken
    })

    const { access_token, refresh_token: newRefreshToken } = response.data
    saveTokens(access_token, newRefreshToken)

    return response.data
  } catch (error) {
    // Если refresh token невалиден, очищаем токены
    clearTokens()
    return null
  }
}

/**
 * Получение профиля пользователя
 */
export async function getProfile(): Promise<UserProfile> {
  const response = await apiClient.get<UserProfile>('/auth/profile')
  return response.data
}

/**
 * Проверка наличия токена авторизации
 */
export function isAuthenticated(): boolean {
  return getAccessToken() !== null
}
