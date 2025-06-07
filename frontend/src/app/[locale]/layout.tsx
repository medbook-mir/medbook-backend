import type { Metadata } from "next";
import AntdProvider from "@/providers/antd-provider";
import Header from "@/components/header";
import Footer from "@/components/footer";
import ScrollToTop from "@/components/basic/scroll-to-top";
import BackToTop from "@/components/basic/back-to-top";
import { NextIntlClientProvider } from "next-intl";
import { notFound } from "next/navigation";
import { i18nConfig } from "@/i18n/config";
import "../globals.css";

export const metadata: Metadata = {
  title: "MedVisit",
  description: "MedVisit - Your Health Partner",
};

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  let messages;
  try {
    messages = (await import(`../../../messages/${locale}.json`)).default;
  } catch (error) {
    notFound();
  }

  if (!i18nConfig.locales.includes(locale as any)) {
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
