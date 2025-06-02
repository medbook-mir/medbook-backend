"use client";

import {
  CssBaseline,
  InitColorSchemeScript,
  ThemeProvider
} from "@mui/material";
import React from "react";
import theme from "./theme";

function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      <InitColorSchemeScript attribute="class" />
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </>
  );
}

export default Providers;
