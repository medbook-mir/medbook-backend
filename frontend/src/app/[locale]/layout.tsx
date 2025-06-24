'use client";';

import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { routing, Locale } from "@/i18n/routing";
import { ClientProviders } from "../../layout/client-providers";
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
        <ClientProviders locale={locale} messages={messages}>
          {children}
        </ClientProviders>
      </body>
    </html>
  );
}
