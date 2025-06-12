import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";
import typography from "@tailwindcss/typography";
import type { PluginAPI } from "tailwindcss/plugin";

type CSSRuleObject = Record<string, any>;

const fontConfig = {
  h1: {
    fontFamily: "poppins",
    fontSize: "48px",
    fontWeight: "600",
    lineHeight: "100%",
    letterSpacing: "0",
  },
  h2bold: {
    fontFamily: "poppins",
    fontSize: "3rem", //48px
    fontWeight: "700",
    lineHeight: "100%",
    letterSpacing: "0",
  },
  h2: {
    fontFamily: "poppins",
    fontSize: "3rem", //48px
    fontWeight: "medium",
    lineHeight: "3.6rem",
    letterSpacing: "0",
  },
  h3bold: {
    fontFamily: "poppins",
    fontSize: "2.5rem", //40px
    fontWeight: "bold",
    lineHeight: "3rem",
    letterSpacing: "0",
  },
  h3: {
    fontFamily: "poppins",
    fontSize: "2.5rem", //40px
    fontWeight: "medium",
    lineHeight: "3rem",
    letterSpacing: "0",
  },
  h4bold: {
    fontFamily: "poppins",
    fontSize: "2rem", //32px
    fontWeight: "bold",
    lineHeight: "2.4rem",
    letterSpacing: "0",
  },
  h4: {
    fontFamily: "poppins",
    fontSize: "2rem", //32px
    fontWeight: "medium",
    lineHeight: "2.4rem",
    letterSpacing: "0",
  },
  h5lg: {
    fontFamily: "poppins",
    fontSize: "1.5rem", //24px
    fontWeight: "medium",
    lineHeight: "1.8rem",
    letterSpacing: "0",
  },
  h5: {
    fontFamily: "poppins",
    fontSize: "1.25rem", //20px
    fontWeight: "medium",
    lineHeight: "1.8rem",
    letterSpacing: "0",
  },
  h6lg: {
    fontFamily: "poppins",
    fontSize: "1.125rem", //18px
    fontWeight: "medium",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  h6: {
    fontFamily: "poppins",
    fontSize: "1rem", //16px
    fontWeight: "medium",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  small: {
    fontFamily: "poppins",
    fontSize: "0.75rem", //12px
    fontWeight: "inherit",
    lineHeight: "1.125rem",
    letterSpacing: "0",
  },
  body: {
    fontFamily: "poppins",
    fontSize: "0.875rem", //14px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-l": {
    fontFamily: "poppins",
    fontSize: "1rem", //16px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-xl": {
    fontFamily: "poppins",
    fontSize: "1.125rem", //18px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-xxl": {
    fontFamily: "poppins",
    fontSize: "1.5rem",
    fontWeight: "inherit",
    lineHeight: "2rem",
    letterSpacing: "0",
  },
};

const getTypography = (theme: PluginAPI["theme"]) =>
  Object.fromEntries(
    Object.entries(fontConfig).map(([k, v]) => [
      `.typography-${k}`,
      {
        ...v,
        fontFamily: theme(`fontFamily.` + v.fontFamily),
        fontWeight: theme("fontWeight." + v.fontWeight),
      } as CSSRuleObject,
    ])
  );

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        hauss: ["poppins", "sans-serif"],
      },
      rotate: {
        270: "-90deg",
      },
      gridTemplateColumns: {
        "1_2_1": "1fr 2fr 1fr",
        "1_2": "1fr 2fr",
      },
      colors: {
        primary: "#046D5F",
        secondary: "#0D0D0D",
      },
      backgroundImage: {
        "gradient-primary": "linear-gradient(to right, #046D5F, #1549BD)",
      },
      padding: {
        card: "65px",
        container: "240px",
      },
      margin: {
        card: "65px",
        container: "240px",
      },
      boxShadow: {
        button: "4px 4px 12px rgba(0,0,0,0.2)",
        steps: "0px 0px 32px var(--tw-shadow-color)",
        inset: "inset 0 0 0 1.6px #046D5F",
      },
      borderRadius: {
        primary: "16px",
        secondary: "12px",
        input: "8px",
      },
      maxWidth: {
        container: "1440px",
      },
      spacing: {
        card: "64px",
      },
      screens: {
        xl: "1280px",
        "2xl": "1440px",
      },
    },
  },
  plugins: [
    plugin(({ addBase, addComponents, theme }) => {
      const typographyComponents = getTypography(theme);
      addComponents(typographyComponents);
      addBase({
        "html, body": {
          "@apply typography-body-l": {},
          lineHeight: "inherit",
        },
        textarea: {
          resize: "none",
        },
      });
    }),
    plugin(({ addUtilities }) => {
      addUtilities({
        ".contain-strict": {
          contain: "strict",
        },
      });
    }),
    function ({ addVariant }: PluginAPI) {
      addVariant("child", "& > *");
      addVariant("child-hover", "& > *:hover");
    },
    typography,
  ],
};

export default config;
