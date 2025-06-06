"use client";

import { useParams, useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { i18nConfig, type Locale } from "@/i18n";
import i18next from "@/i18n";

type LanguageProviderProps = {
  children: React.ReactNode;
};

const LanguageProvider = ({ children }: LanguageProviderProps) => {
  const { lang } = useParams();
  const router = useRouter();
  const pathname = usePathname();
  const [isI18nInitialized, setIsI18nInitialized] = useState(false);

  useEffect(() => {
    const initI18n = async () => {
      await i18next.init();
      setIsI18nInitialized(true);
    };

    if (!i18next.isInitialized) {
      initI18n();
    } else {
      setIsI18nInitialized(true);
    }
  }, []);

  useEffect(() => {
    if (!isI18nInitialized) return;

    const handleLanguageChange = async () => {
      try {
        if (!lang || !i18nConfig.locales.includes(lang as Locale)) {
          const savedLang =
            typeof window !== "undefined"
              ? localStorage.getItem("language")
              : null;

          const targetLang =
            savedLang && i18nConfig.locales.includes(savedLang as Locale)
              ? (savedLang as Locale)
              : i18nConfig.defaultLocale;

          await i18next.changeLanguage(targetLang);

          // Only redirect if we're not already on the correct language path
          if (!pathname.startsWith(`/${targetLang}`)) {
            const newPathname =
              pathname === "/"
                ? `/${targetLang}`
                : pathname.replace(/^\/[^/]+/, `/${targetLang}`);

            router.replace(newPathname);
          }
        } else {
          await i18next.changeLanguage(lang as Locale);
          if (typeof window !== "undefined") {
            localStorage.setItem("language", lang as Locale);
          }
        }
      } catch (error) {
        console.error("Error changing language:", error);
        await i18next.changeLanguage(i18nConfig.defaultLocale);
      }
    };

    handleLanguageChange();
  }, [lang, router, pathname, isI18nInitialized]);

  if (!isI18nInitialized) {
    return null;
  }

  return <>{children}</>;
};

export default LanguageProvider;
