import { createSlice, PayloadAction } from "@reduxjs/toolkit";

const modalsNames = {
  loginModal: "loginModal",
  registerModal: "registerModal",
  sessionExpiredModal: "sessionExpiredModal",
};

type ModalsState = { modals: { [K in keyof typeof modalsNames]: boolean } };

const defaultState: ModalsState = {
  modals: {
    loginModal: false,
    registerModal: false,
    sessionExpiredModal: false,
  },
};

const slice = createSlice({
  name: "modals",
  initialState: defaultState,
  reducers: {
    openModal: (state, action: PayloadAction<keyof typeof modalsNames>) => {
      state.modals[action.payload] = true;
    },
    closeModal: (state, action: PayloadAction<keyof typeof modalsNames>) => {
      state.modals[action.payload] = false;
    },
  },
});

export const { openModal, closeModal } = slice.actions;
export default slice.reducer;
