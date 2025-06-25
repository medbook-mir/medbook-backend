import { TokenService } from "@/utils/storage";
import { createSlice } from "@reduxjs/toolkit";
import { logoutThunk } from "../thunks/authThunk";

export type AuthState = {
  auth: {
    token: string;
    refreshToken: string;
    status: "loading" | "idle" | "failed" | "success";
  };
  isLoading: boolean;
};

const defaultState: AuthState = {
  auth: {
    token: "",
    refreshToken: "",
    status: "idle",
  },
  isLoading: false,
};

const slice = createSlice({
  name: "auth",
  initialState: defaultState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(logoutThunk.pending, (state) => {
      state.auth = { ...defaultState.auth };
      TokenService.clearTokens();
      state.isLoading = false;
    });
  },
});

const { reducer } = slice;
export default reducer;
