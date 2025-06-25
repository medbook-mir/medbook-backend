import AuthAPI from "@/api/v1/authAPI";
import { LoginBodyType, RegisterBodyType } from "@/types";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const registerThunk = createAsyncThunk(
  "register",
  async (body: RegisterBodyType, { rejectWithValue }) => {
    try {
      const data = await AuthAPI.register(body);
      return data.data;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data || error.message || "Register xatosi"
      );
    }
  }
);

export const loginThunk = createAsyncThunk(
  "login",
  async (body: LoginBodyType, { rejectWithValue }) => {
    try {
      const data = await AuthAPI.login(body);
      return data.data;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data || error.message || "Login xatosi"
      );
    }
  }
);

export const logoutThunk = createAsyncThunk("logout", async () => {
  const result = await AuthAPI.logout();

  return result;
});
