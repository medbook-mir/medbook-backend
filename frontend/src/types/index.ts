declare global {
  interface Window {
    ymaps: any
  }
}

export type LoginBodyType = {
  login: string
  password: string
}

export type RegisterFormType = {
  email: string
  name: string
  birthday: string
  password: string
  confirmPassword?: string
}

export type RegisterBodyType = {
  email: string
  name: string
  birthday: string
  password: string
}

export interface LoginResponseType {
  accessToken: string
  refreshToken: string
  accessTokenExpiry: number
  refreshTokenExpiry: number
  actionRequired?: boolean
}

export interface ApiResponseWithContent<T> {
  result: T
  success: boolean
}
