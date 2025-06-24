import { RootState } from '../store'

export const getUserState = (state: RootState) => state.user

export const getMe = (state: RootState) => state.user.user

export const getIsAuthenticated = (state: RootState) => state.user.isAuthed
