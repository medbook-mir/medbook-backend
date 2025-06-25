import userAPI from "@/api/v1/userAPI";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getMeThunk = createAsyncThunk("getMe", async () => {
  const data = await userAPI.getMe();

  return data.data;
});
