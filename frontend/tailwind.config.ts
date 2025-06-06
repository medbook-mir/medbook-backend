import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";
import typography from "@tailwindcss/typography";
import type { PluginAPI } from "tailwindcss/plugin";

type CSSRuleObject = Record<string, any>;

const fontConfig = {
  h1bold: {
    fontFamily: "hauss",
    fontSize: "4rem", // 64px
    fontWeight: "black",
    lineHeight: "4rem",
    letterSpacing: "0",
  },
  h1: {
    fontFamily: "hauss",
    fontSize: "4rem", //64px
    fontWeight: "bold",
    lineHeight: "4rem",
    letterSpacing: "0",
  },
  h2bold: {
    fontFamily: "hauss",
    fontSize: "3rem", //48px
    fontWeight: "bold",
    lineHeight: "3.6rem",
    letterSpacing: "0",
  },
  h2: {
    fontFamily: "hauss",
    fontSize: "3rem", //48px
    fontWeight: "medium",
    lineHeight: "3.6rem",
    letterSpacing: "0",
  },
  h3bold: {
    fontFamily: "hauss",
    fontSize: "2.5rem", //40px
    fontWeight: "bold",
    lineHeight: "3rem",
    letterSpacing: "0",
  },
  h3: {
    fontFamily: "hauss",
    fontSize: "2.5rem", //40px
    fontWeight: "medium",
    lineHeight: "3rem",
    letterSpacing: "0",
  },
  h4bold: {
    fontFamily: "hauss",
    fontSize: "2rem", //32px
    fontWeight: "bold",
    lineHeight: "2.4rem",
    letterSpacing: "0",
  },
  h4: {
    fontFamily: "hauss",
    fontSize: "2rem", //32px
    fontWeight: "medium",
    lineHeight: "2.4rem",
    letterSpacing: "0",
  },
  h5lg: {
    fontFamily: "hauss",
    fontSize: "1.5rem", //24px
    fontWeight: "medium",
    lineHeight: "1.8rem",
    letterSpacing: "0",
  },
  h5: {
    fontFamily: "hauss",
    fontSize: "1.25rem", //20px
    fontWeight: "medium",
    lineHeight: "1.8rem",
    letterSpacing: "0",
  },
  h6lg: {
    fontFamily: "hauss",
    fontSize: "1.125rem", //18px
    fontWeight: "medium",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  h6: {
    fontFamily: "hauss",
    fontSize: "1rem", //16px
    fontWeight: "medium",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  small: {
    fontFamily: "hauss",
    fontSize: "0.75rem", //12px
    fontWeight: "inherit",
    lineHeight: "1.125rem",
    letterSpacing: "0",
  },
  body: {
    fontFamily: "hauss",
    fontSize: "0.875rem", //14px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-l": {
    fontFamily: "hauss",
    fontSize: "1rem", //16px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-xl": {
    fontFamily: "hauss",
    fontSize: "1.125rem", //18px
    fontWeight: "inherit",
    lineHeight: "1.5rem",
    letterSpacing: "0",
  },
  "body-xxl": {
    fontFamily: "hauss",
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
        hauss: ["hauss", "sans-serif"],
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
        secondary: "#fff",
      },
      backgroundImage: {
        "gradient-primary": "linear-gradient(to right, #4D83FB, #1549BD)",
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
        button: "5px 5px 10px rgba(0,0,0,0.2)",
        steps: "0px 0px 30px var(--tw-shadow-color)",
        inset: "inset 0 0 0 1.5px #3871F0",
      },
      borderRadius: {
        primary: "15px",
        secondary: "10px",
        input: "6px",
      },
      maxWidth: {
        container: "1920px",
      },
      spacing: {
        card: "65px",
      },
      screens: {
        "1.5xl": "1440px",
        "2xl": "1920px",
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
