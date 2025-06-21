'use client";';

import type { Metadata } from "next";
import { NextIntlClientProvider } from "next-intl";
import { notFound } from "next/navigation";
import AntdProvider from "@/providers/antd-provider";
import FooterWrapper from "@/components/layout/footer-wrapper";
import ScrollToTop from "@/components/basic/scroll-to-top";
import BackToTop from "@/components/basic/back-to-top";
import { routing, Locale } from "@/i18n/routing";
import "../globals.css";

export const metadata: Metadata = {
  title: "MedVisit",
  description: "MedVisit - Your Health Partner",
};

async function getMessages(locale: string) {
  try {
    return (await import(`../../../messages/${locale}.json`)).default;
  } catch (error) {
    notFound();
  }
}

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: Locale }>;
}) {
  const { locale } = await params;

  if (!routing.locales.includes(locale)) {
    notFound();
  }

  const messages = await getMessages(locale);

  return (
    <html lang={locale}>
      <body className="mx-auto flex min-h-screen w-full max-w-container flex-col justify-between overflow-x-hidden">
        <NextIntlClientProvider locale={locale} messages={messages}>
          <AntdProvider>
            <main className="flex-1">{children}</main>
            <FooterWrapper />
            <ScrollToTop />
            <BackToTop />
          </AntdProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
