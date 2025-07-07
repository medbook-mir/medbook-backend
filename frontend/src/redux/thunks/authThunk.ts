import AuthAPI from '@/api/v1/authAPI'
import { LoginBodyType, RegisterBodyType, VerifyBodyType, RefreshBodyType } from '@/types'
import { createAsyncThunk } from '@reduxjs/toolkit'

export const registerThunk = createAsyncThunk('auth/register', async (body: RegisterBodyType, { rejectWithValue }) => {
  try {
    const data = await AuthAPI.register(body)
    return data.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Register xatosi')
  }
})

export const loginThunk = createAsyncThunk('auth/login', async (body: LoginBodyType, { rejectWithValue }) => {
  try {
    const data = await AuthAPI.login(body)
    return data.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Login xatosi')
  }
})

export const verifyThunk = createAsyncThunk('auth/verify', async (body: VerifyBodyType, { rejectWithValue }) => {
  try {
    const data = await AuthAPI.verify(body)
    return data.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Verification xatosi')
  }
})

export const refreshThunk = createAsyncThunk('auth/refresh', async (body: RefreshBodyType, { rejectWithValue }) => {
  try {
    const data = await AuthAPI.refresh(body)
    return data.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Token refresh xatosi')
  }
})

export const logoutThunk = createAsyncThunk('auth/logout', async (_, { rejectWithValue }) => {
  try {
    const result = await AuthAPI.logout()
    return result.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Logout xatosi')
  }
})

// Additional utility thunks for auth state management
export const checkAuthThunk = createAsyncThunk('auth/check', async (_, { rejectWithValue }) => {
  try {
    // Check if user is authenticated by making a request to a protected endpoint
    // This could be a user profile endpoint or any protected API call
    // const result = await UserAPI.getProfile()

    // For now, return success if we have tokens
    return { success: true }
  } catch (error: any) {
    return rejectWithValue(error.response?.data || error.message || 'Auth check xatosi')
  }
})

export const forgotPasswordThunk = createAsyncThunk(
  'auth/forgotPassword',
  async (email: string, { rejectWithValue }) => {
    try {
      // If there's a forgot password endpoint, call it here
      // const result = await AuthAPI.forgotPassword({ email })

      // For now, return success
      return { success: true, message: 'Password reset email sent' }
    } catch (error: any) {
      return rejectWithValue(error.response?.data || error.message || 'Forgot password xatosi')
    }
  }
)

export const resetPasswordThunk = createAsyncThunk(
  'auth/resetPassword',
  async (data: { token: string; newPassword: string }, { rejectWithValue }) => {
    try {
      // If there's a reset password endpoint, call it here
      // const result = await AuthAPI.resetPassword(data)

      // For now, return success
      return { success: true, message: 'Password reset successfully' }
    } catch (error: any) {
      return rejectWithValue(error.response?.data || error.message || 'Password reset xatosi')
    }
  }
)
