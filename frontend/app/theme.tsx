"use client";
import { createTheme } from "@mui/material/styles";
import { Poppins } from "next/font/google";

const poppins = Poppins({
  weight: ["300", "400", "500", "700"],
  subsets: ["latin"],
  display: "swap"
});

const theme = createTheme({
  colorSchemes: { light: true, dark: false },
  cssVariables: {
    colorSchemeSelector: "class"
  },
  typography: {
    fontFamily: poppins.style.fontFamily
  },
  components: {
    MuiAlert: {
      styleOverrides: {
        root: {
          variants: [
            {
              props: { severity: "info" },
              style: {
                backgroundColor: "#046D5F"
              }
            }
          ]
        }
      }
    }
  }
});

export default theme;
