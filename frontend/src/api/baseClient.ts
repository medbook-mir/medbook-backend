import Axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { buildParams } from './helpers'
import { TokenService } from '@/utils/storage'
import { env } from '@/utils/env'
import { getLocale } from 'next-intl/server'

const API_URL = env.NEXT_API_URL

declare module 'axios' {
  export interface AxiosRequestConfig {
    _retry?: boolean
    unhandled?: boolean
  }
}

export class HTTPError extends Error {
  constructor(
    public status: number,
    public cause: string
  ) {
    super(cause)
  }
}
export class BaseClient {
  private baseUrl = API_URL
  private axios: AxiosInstance
  private isRefreshing = false
  private refreshSubscribers: ((token: string) => void)[] = []
  private static instance: BaseClient | null = null

  private constructor() {
    this.axios = Axios.create({
      baseURL: this.baseUrl
    })

    // Request interceptor for attaching the token
    this.axios.interceptors.request.use(this.attachToken)
    // Response interceptor for handling errors
    this.axios.interceptors.response.use((response: AxiosResponse) => response, this.onApiError)
  }

  public static getInstance(): BaseClient {
    if (!BaseClient.instance) {
      BaseClient.instance = new BaseClient()
    }
    return BaseClient.instance
  }

  // Request interceptor for attaching token
  private attachToken = async (req: InternalAxiosRequestConfig) => {
    const token = TokenService.getToken()
    const accessTokenExpiry = TokenService.getAccessTokenExpiry()
    const currentTime = Date.now() / 1000

    if (token && currentTime < accessTokenExpiry) {
      req.headers = req.headers || {}
      req.headers['Authorization'] = `Bearer ${token}`
    }

    // Automatically get current locale and set it in Lang header
    const locale = await getLocale()
    req.headers['Lang'] = locale

    return req
  }

  // API Error handler
  private onApiError = async (error: AxiosError) => {
    const originalRequest = error.config

    if (originalRequest && !originalRequest._retry) {
      originalRequest._retry = true // Faqat bir marta urinish uchun
      switch (error.response?.status) {
        case 401: {
          const success = await this.refreshToken()
          if (success) {
            const newToken = TokenService.getToken()
            if (newToken) {
              originalRequest.headers['Authorization'] = `Bearer ${newToken}`
              return this.axios(originalRequest) // Faqat 1 marta qayta yuborish
            }
          }
          break
        }
        case 502:
          return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }

  // Refresh token method
  private refreshToken = async (): Promise<boolean> => {
    if (this.isRefreshing) {
      return new Promise((resolve) => {
        this.refreshSubscribers.push(() => resolve(true))
      })
    }

    this.isRefreshing = true
    try {
      const refreshToken = TokenService.getRefreshToken()
      const refreshTokenExpiry = TokenService.getRefreshTokenExpiry()
      const currentTime = Date.now() / 1000

      if (!refreshToken || currentTime >= refreshTokenExpiry) {
        TokenService.clearTokens()
        return false
      }

      const response = await this.axios.post('/auth/refresh', { refreshToken })

      const newAccessToken = response.data.accessToken
      const newRefreshToken = response.data.refreshToken
      const newAccessTokenExpiry = response.data.accessTokenExpiry
      const newRefreshTokenExpiry = response.data.refreshTokenExpiry

      TokenService.setToken(newAccessToken, newRefreshToken, newAccessTokenExpiry, newRefreshTokenExpiry)

      this.refreshSubscribers.forEach((callback) => callback(newAccessToken))
      this.refreshSubscribers = []

      return true
    } catch (error) {
      console.warn('refreshToken error:', error)
      TokenService.clearTokens()
      return false
    } finally {
      this.isRefreshing = false
    }
  }

  setAccessToken = (token: string) => {
    const newToken = `Bearer ${token}`
    this.axios.defaults.headers.common.Authorization = newToken

    return newToken
  }

  get = async <T, K, C>(url: string, params?: K, config?: AxiosRequestConfig<C>): Promise<AxiosResponse<T>> => {
    const queryParams = params ? buildParams(params) : ''
    return this.axios.get(url + queryParams, config)
  }

  delete = async <T, K>(url: string, data?: K, body?: K): Promise<AxiosResponse<T>> => {
    return this.axios.delete(url, { params: data, data: body })
  }

  post = async <T, K>(url: string, data?: K, config?: AxiosRequestConfig<K>): Promise<AxiosResponse<T>> => {
    return this.axios.post(url, data, config)
  }

  patch = async <T, K>(url: string, data?: K, config?: AxiosRequestConfig<K>): Promise<AxiosResponse<T>> => {
    return this.axios.patch(url, data, config)
  }

  put = async <T, K>(url: string, data?: K, config?: AxiosRequestConfig<K>): Promise<AxiosResponse<T>> => {
    return this.axios.put(url, data, config)
  }
}

export const baseApiClient = BaseClient.getInstance()
