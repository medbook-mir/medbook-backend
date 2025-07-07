'use client'

import { useMemo } from 'react'
import { NextIntlClientProvider } from 'next-intl'
import { Provider } from 'react-redux'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { store } from '@/redux/store'
import AntdProvider from '@/providers/antd-provider'
import { NotificationProvider } from '@/hooks/useNotification'
import ScrollToTop from '@/components/basic/scroll-to-top'
import BackToTop from '@/components/basic/back-to-top'
import { Locale } from '@/i18n/routing'
import AOSProvider from '@/providers/aos-provider'
import ProtectedComponent from '@/providers/protected-component'
import Header from '@/components/header'
import Footer from '@/components/footer'
import LoginModal from '@/modals/login-modal'
import RegisterModal from '@/modals/register-modal'
import VerifyModal from '@/modals/verify-modal'

interface ClientProvidersProps {
  children: React.ReactNode
  locale: Locale
  messages: any
}

export function ClientProviders({ children, locale, messages }: ClientProvidersProps) {
  const queryClient = useMemo(() => new QueryClient(), [])

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <AntdProvider>
        <QueryClientProvider client={queryClient}>
          <Provider store={store}>
            <AOSProvider>
              <NotificationProvider>
                <ProtectedComponent>
                  <Header />
                </ProtectedComponent>
                <main>{children}</main>
                <ProtectedComponent paths={['/settings']}>
                  <Footer />
                </ProtectedComponent>
                <ScrollToTop />
                <BackToTop />
                <LoginModal />
                <RegisterModal />
                <VerifyModal />
              </NotificationProvider>
            </AOSProvider>
          </Provider>
        </QueryClientProvider>
      </AntdProvider>
    </NextIntlClientProvider>
  )
}
