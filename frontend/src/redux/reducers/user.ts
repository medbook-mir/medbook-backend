import { UserType } from "@/types/user-type";
import { createSlice } from "@reduxjs/toolkit";
import { getMeThunk } from "../thunks/userThunk";
import { loginThunk } from "../thunks/authThunk";

export type UserState = {
  user: UserType | null;
  isAuthed: boolean;
  getMeLoading: boolean;
  actionRequired?: boolean;
};

const initialState: UserState = {
  user: null,
  isAuthed: false,
  getMeLoading: false,
  actionRequired: false,
};

const slice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
      state.isAuthed = true;
    },
    clearUser: (state) => {
      state.user = null;
      state.isAuthed = false;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getMeThunk.pending, (state) => {
      state.getMeLoading = true;
    });
    builder.addCase(getMeThunk.fulfilled, (state, action) => {
      state.user = action.payload.result;
      state.isAuthed = true;
      state.getMeLoading = false;
      state.actionRequired = action.payload.result.actionRequired;
    });
    builder.addCase(getMeThunk.rejected, (state) => {
      state.getMeLoading = false;
    });
    builder.addCase(loginThunk.fulfilled, (state, action) => {
      state.isAuthed = true;
      state.actionRequired = action.payload.result.actionRequired;
    });
  },
});

const { actions, reducer } = slice;
export const { setUser, clearUser } = actions;
export default reducer;
