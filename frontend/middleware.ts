import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { i18nConfig, type Locale } from "./src/i18n";

export function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;

  // Static files, API routes va maxsus yo'llarni o'tkazib yuborish
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.includes(".well-known") ||
    pathname.includes(".") ||
    pathname === "/favicon.ico"
  ) {
    return NextResponse.next();
  }

  // URL'da til prefixi borligini tekshirish
  const pathnameHasLocale = i18nConfig.locales.some(
    (locale: Locale) =>
      pathname === `/${locale}` || pathname.startsWith(`/${locale}/`)
  );

  if (pathnameHasLocale) return NextResponse.next();

  // Foydalanuvchi tilini aniqlash
  let locale: Locale = i18nConfig.defaultLocale;
  const cookieLocale = request.cookies.get("language")?.value;
  const acceptLanguage = request.headers.get("accept-language");

  if (cookieLocale && i18nConfig.locales.includes(cookieLocale as Locale)) {
    locale = cookieLocale as Locale;
  } else if (acceptLanguage) {
    const preferredLocale = acceptLanguage
      .split(",")[0]
      .split("-")[0]
      .toLowerCase();

    if (i18nConfig.locales.includes(preferredLocale as Locale)) {
      locale = preferredLocale as Locale;
    }
  }

  // Yangi URL yaratish
  const newUrl = new URL(
    `/${locale}${pathname.startsWith("/") ? pathname : `/${pathname}`}${search}`,
    request.url
  );

  // 307 Temporary Redirect bilan yo'naltirish
  return NextResponse.redirect(newUrl, 307);
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    "/((?!_next|api|.*\\..*|.well-known).*)",
    // Optional: Match all root level pages
    "/",
  ],
};
