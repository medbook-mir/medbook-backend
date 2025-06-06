import type { Metadata } from "next";
import AntdProvider from "@/providers/antd-provider";
import Header from "@/components/header";
import Footer from "@/components/footer";
import LanguageProvider from "@/providers/language-provider";
import ScrollToTop from "@/components/basic/scroll-to-top";
import BackToTop from "@/components/basic/back-to-top";
import "../globals.css";

export const metadata: Metadata = {
  title: "MedVisit",
  description: "MedVisit - Your Health Partner",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={` mx-auto flex min-h-screen w-full max-w-container flex-col justify-between overflow-x-hidden`}
      >
        <AntdProvider>
          <LanguageProvider>
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
            <ScrollToTop />
            <BackToTop />
          </LanguageProvider>
        </AntdProvider>
      </body>
    </html>
  );
}
