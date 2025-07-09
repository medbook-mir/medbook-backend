'use client'

import { useTranslations } from 'next-intl'
import { useMemo } from 'react'
import { CustomBreadcrumb } from '@/components/ui/breadcrumb'
import { Container } from '@/theme/container'
import { usePathname } from '@/i18n/navigation'
import Sidebar from '@/components/settings/sidebar'
import { sidebarData } from '@/components/settings/sidebar-data'

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  const t = useTranslations('settingsLayout')
  const pathname = usePathname()

  const currentPath = useMemo(() => {
    return sidebarData.find((item) => pathname.includes(item.href))
  }, [pathname])

  return (
    <section className="overflow-x-hidden py-10">
      <Container>
        <CustomBreadcrumb
          pages={[
            { title: t('settings'), href: `/settings` },
            { title: t(currentPath?.title ?? ''), href: `/settings/${currentPath?.href}` }
          ]}
        />
        <h1 className="mt-4 mb-8 text-[24px] leading-[127%] font-bold">Settings</h1>
        <div className="grid grid-cols-[320px_1fr] items-start gap-6">
          <Sidebar />
          <div className="rounded-2xl border-2 border-[#E9ECF4]">{children}</div>
        </div>
      </Container>
    </section>
  )
}
