import type { Metadata } from "next";
import { NextIntlClientProvider } from "next-intl";
import { notFound } from "next/navigation";
import { getMessages } from "next-intl/server";
import AntdProvider from "@/providers/antd-provider";
import Header from "@/components/header";
import Footer from "@/components/footer";
import ScrollToTop from "@/components/basic/scroll-to-top";
import BackToTop from "@/components/basic/back-to-top";
import { routing, Locale } from "@/i18n/routing";
import "./globals.css";

export const metadata: Metadata = {
  title: "MedVisit",
  description: "MedVisit - Your Health Partner"
};

export default async function RootLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: Locale }>;
}) {
  const { locale } = await params;

  if (!routing.locales.includes(locale)) {
    notFound();
  }

  let messages;
  try {
    messages = await getMessages();
  } catch (error) {
    notFound();
  }

  return (
    <html lang={locale}>
      <body className="mx-auto flex min-h-screen w-full max-w-container flex-col justify-between overflow-x-hidden">
        <NextIntlClientProvider locale={locale} messages={messages}>
          <AntdProvider>
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
            <ScrollToTop />
            <BackToTop />
          </AntdProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
