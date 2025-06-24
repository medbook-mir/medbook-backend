"use client";

import { useMemo } from "react";
import { NextIntlClientProvider } from "next-intl";
import { Provider } from "react-redux";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { store } from "@/redux/store";
import AntdProvider from "@/providers/antd-provider";
import FooterWrapper from "@/components/layout/footer-wrapper";
import { NotificationProvider } from "@/hooks/useNotification";
import ScrollToTop from "@/components/basic/scroll-to-top";
import BackToTop from "@/components/basic/back-to-top";
import { Locale } from "@/i18n/routing";

interface ClientProvidersProps {
  children: React.ReactNode;
  locale: Locale;
  messages: any;
}

export function ClientProviders({
  children,
  locale,
  messages,
}: ClientProvidersProps) {
  const queryClient = useMemo(() => new QueryClient(), []);

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <AntdProvider>
        <QueryClientProvider client={queryClient}>
          <Provider store={store}>
            <NotificationProvider>
              <main className="flex-1">{children}</main>
              <FooterWrapper />
              <ScrollToTop />
              <BackToTop />
            </NotificationProvider>
          </Provider>
        </QueryClientProvider>
      </AntdProvider>
    </NextIntlClientProvider>
  );
}
