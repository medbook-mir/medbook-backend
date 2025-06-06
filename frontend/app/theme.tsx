"use client";
import { createTheme } from "@mui/material/styles";
import { Poppins } from "next/font/google";

const poppins = Poppins({
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
  display: "swap"
});

const theme = createTheme({
  palette: {
    primary: {
      main: "#046D5F",
      contrastText: "#FFFFFF"
    },
    secondary: {
      main: "#F2F2F2",
      contrastText: "#000000"
    },
    background: {
      default: "#FFFFFF",
      paper: "#F2F2F2"
    },
    text: {
      primary: "#0D0D0D",
      secondary: "#565656"
    }
  },
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
