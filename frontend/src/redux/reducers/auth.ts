import { TokenService } from '@/utils/storage'
import { createSlice } from '@reduxjs/toolkit'
import {
  loginThunk,
  registerThunk,
  logoutThunk,
  verifyThunk,
  refreshThunk,
  checkAuthThunk,
  forgotPasswordThunk,
  resetPasswordThunk
} from '../thunks/authThunk'

export type AuthState = {
  auth: {
    token: string
    refreshToken: string
    status: 'loading' | 'idle' | 'failed' | 'success'
  }
  isLoading: boolean
  error: string | null
  user: any | null
}

const defaultState: AuthState = {
  auth: {
    token: '',
    refreshToken: '',
    status: 'idle'
  },
  isLoading: false,
  error: null,
  user: null
}

const slice = createSlice({
  name: 'auth',
  initialState: defaultState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    clearAuth: (state) => {
      state.auth = { ...defaultState.auth }
      state.user = null
      TokenService.clearTokens()
    }
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
        state.auth.status = 'loading'
      })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.isLoading = false
        state.auth.status = 'success'
        state.auth.token = action.payload.result.accessToken
        state.auth.refreshToken = action.payload.result.refreshToken
        TokenService.setToken(
          action.payload.result.accessToken,
          action.payload.result.refreshToken,
          action.payload.result.accessTokenExpiry,
          action.payload.result.refreshTokenExpiry
        )
      })
      .addCase(loginThunk.rejected, (state, action) => {
        state.isLoading = false
        state.auth.status = 'failed'
        state.error = (action.payload as string) || 'Login failed'
      })

    // Register
    builder
      .addCase(registerThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
        state.auth.status = 'loading'
      })
      .addCase(registerThunk.fulfilled, (state, action) => {
        state.isLoading = false
        state.auth.status = 'success'
        state.auth.token = action.payload.result.accessToken
        state.auth.refreshToken = action.payload.result.refreshToken
        TokenService.setToken(
          action.payload.result.accessToken,
          action.payload.result.refreshToken,
          action.payload.result.accessTokenExpiry,
          action.payload.result.refreshTokenExpiry
        )
      })
      .addCase(registerThunk.rejected, (state, action) => {
        state.isLoading = false
        state.auth.status = 'failed'
        state.error = (action.payload as string) || 'Registration failed'
      })

    // Verify
    builder
      .addCase(verifyThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(verifyThunk.fulfilled, (state, action) => {
        state.isLoading = false
        state.auth.token = action.payload.result.accessToken
        state.auth.refreshToken = action.payload.result.refreshToken
        TokenService.setToken(
          action.payload.result.accessToken,
          action.payload.result.refreshToken,
          action.payload.result.accessTokenExpiry,
          action.payload.result.refreshTokenExpiry
        )
      })
      .addCase(verifyThunk.rejected, (state, action) => {
        state.isLoading = false
        state.error = (action.payload as string) || 'Verification failed'
      })

    // Refresh
    builder
      .addCase(refreshThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(refreshThunk.fulfilled, (state, action) => {
        state.isLoading = false
        state.auth.token = action.payload.result.accessToken
        state.auth.refreshToken = action.payload.result.refreshToken
        TokenService.setToken(
          action.payload.result.accessToken,
          action.payload.result.refreshToken,
          action.payload.result.accessTokenExpiry,
          action.payload.result.refreshTokenExpiry
        )
      })
      .addCase(refreshThunk.rejected, (state, action) => {
        state.isLoading = false
        state.error = (action.payload as string) || 'Token refresh failed'
        // If refresh fails, clear auth state
        state.auth = { ...defaultState.auth }
        TokenService.clearTokens()
      })

    // Logout
    builder
      .addCase(logoutThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(logoutThunk.fulfilled, (state) => {
        state.isLoading = false
        state.auth = { ...defaultState.auth }
        state.user = null
        TokenService.clearTokens()
      })
      .addCase(logoutThunk.rejected, (state, action) => {
        state.isLoading = false
        state.error = (action.payload as string) || 'Logout failed'
        // Even if logout fails, clear local auth state
        state.auth = { ...defaultState.auth }
        state.user = null
        TokenService.clearTokens()
      })

    // Check Auth
    builder
      .addCase(checkAuthThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(checkAuthThunk.fulfilled, (state) => {
        state.isLoading = false
        state.auth.status = 'success'
      })
      .addCase(checkAuthThunk.rejected, (state, action) => {
        state.isLoading = false
        state.auth.status = 'failed'
        state.error = (action.payload as string) || 'Auth check failed'
        // Clear auth state if check fails
        state.auth = { ...defaultState.auth }
        TokenService.clearTokens()
      })

    // Forgot Password
    builder
      .addCase(forgotPasswordThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(forgotPasswordThunk.fulfilled, (state) => {
        state.isLoading = false
      })
      .addCase(forgotPasswordThunk.rejected, (state, action) => {
        state.isLoading = false
        state.error = (action.payload as string) || 'Forgot password failed'
      })

    // Reset Password
    builder
      .addCase(resetPasswordThunk.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(resetPasswordThunk.fulfilled, (state) => {
        state.isLoading = false
      })
      .addCase(resetPasswordThunk.rejected, (state, action) => {
        state.isLoading = false
        state.error = (action.payload as string) || 'Password reset failed'
      })
  }
})

const { reducer, actions } = slice
export const { clearError, clearAuth } = actions
export default reducer
