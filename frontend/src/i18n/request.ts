import { getRequestConfig } from 'next-intl/server'
import { Locale, routing } from './routing'

export default getRequestConfig(async ({ requestLocale }) => {
  let locale = (await requestLocale) as string | undefined

  if (!locale || !routing.locales.includes(locale as Locale)) {
    locale = routing.defaultLocale
  }

  return {
    locale: locale as Locale,
    messages: (await import(`../messages/${locale}.json`)).default
  }
})
