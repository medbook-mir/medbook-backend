import { createSelector } from "@reduxjs/toolkit";
import { RootState } from "../store";

export const getModals = (state: RootState) => state.modals;

export const getLoginModal = createSelector(
  getModals,
  (modals) => modals.modals.loginModal
);

export const getSessionExpiredModal = createSelector(
  getModals,
  (modals) => modals.modals.sessionExpiredModal
);
