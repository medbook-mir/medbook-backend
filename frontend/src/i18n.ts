import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import HttpApi from "i18next-http-backend";
import LanguageDetector from "i18next-browser-languagedetector";

// i18n configuration
export const i18nConfig = {
  locales: ["en", "uz", "ru"] as const,
  defaultLocale: "en" as const,
  pathnames: {
    "/": "/",
  },
} as const;

export type Locale = (typeof i18nConfig)["locales"][number];
export type Pathnames = keyof (typeof i18nConfig)["pathnames"];

const getInitialLanguage = () => {
  if (typeof window === "undefined") return i18nConfig.defaultLocale;
  return localStorage.getItem("language") || i18nConfig.defaultLocale;
};

i18n
  .use(HttpApi)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    supportedLngs: i18nConfig.locales,
    fallbackLng: i18nConfig.defaultLocale,
    lng: getInitialLanguage(),
    debug: false,
    interpolation: {
      escapeValue: false,
    },
    backend: {
      loadPath: "/locales/{{lng}}/translation.json",
    },
    detection: {
      order: ["path", "cookie", "localStorage", "navigator"],
      lookupFromPathIndex: 0,
      caches: ["localStorage", "cookie"],
      cookieMinutes: 60 * 24 * 365, // 1 yil
    },
  });

export default i18n;
