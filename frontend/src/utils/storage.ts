import * as SessionKeys from '@/constants/session-constants'

export const getFromStorage = (key: string) => {
  return sessionStorage.getItem(key) || localStorage.getItem(key)
}

export class TokenService {
  static getToken() {
    return sessionStorage.getItem(SessionKeys.TOKEN)
  }

  static getRefreshToken() {
    return sessionStorage.getItem(SessionKeys.REFRESH_TOKEN)
  }

  static getAccessTokenExpiry() {
    return parseInt(sessionStorage.getItem(SessionKeys.ACCESS_TOKEN_EXPIRY) || '0', 10)
  }

  static getRefreshTokenExpiry() {
    return parseInt(sessionStorage.getItem(SessionKeys.REFRESH_TOKEN_EXPIRY) || '0', 10)
  }

  static setToken(accessToken: string, refreshToken: string, accessTokenExpiry: number, refreshTokenExpiry: number) {
    const currentTime = Math.floor(Date.now() / 1000)

    sessionStorage.setItem(SessionKeys.TOKEN, accessToken)
    sessionStorage.setItem(SessionKeys.REFRESH_TOKEN, refreshToken)
    sessionStorage.setItem(SessionKeys.ACCESS_TOKEN_EXPIRY, (currentTime + accessTokenExpiry).toString())
    sessionStorage.setItem(SessionKeys.REFRESH_TOKEN_EXPIRY, (currentTime + refreshTokenExpiry).toString())
  }

  static clearTokens() {
    sessionStorage.removeItem(SessionKeys.TOKEN)
    sessionStorage.removeItem(SessionKeys.REFRESH_TOKEN)
    sessionStorage.removeItem(SessionKeys.ACCESS_TOKEN_EXPIRY)
    sessionStorage.removeItem(SessionKeys.REFRESH_TOKEN_EXPIRY)
  }
}

export class UserStorage {
  static getUserId() {
    return sessionStorage.getItem(SessionKeys.USER_ID)
  }

  static getName() {
    return sessionStorage.getItem(SessionKeys.NAME)
  }

  static setUserInfo(userId: string, name: string) {
    sessionStorage.setItem(SessionKeys.USER_ID, userId)
    sessionStorage.setItem(SessionKeys.NAME, name)
  }

  static clearUserInfo() {
    sessionStorage.removeItem(SessionKeys.USER_ID)
    sessionStorage.removeItem(SessionKeys.NAME)
  }
}
