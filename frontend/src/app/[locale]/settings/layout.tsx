'use client";'

import type { Metadata } from 'next'
import { CustomBreadcrumb } from '@/components/ui/breadcrumb'
import { Container } from '@/theme/container'
import Sidebar from '@/components/settings/sidebar'

export const metadata: Metadata = {
  title: {
    default: 'Settings',
    template: '%s | Settings'
  },
  description: 'Manage your settings'
}

export default async function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <section className="overflow-x-hidden py-10">
      <Container>
        <CustomBreadcrumb
          pages={[
            { title: 'Settings', href: `/settings/` },
            { title: 'My Data', href: `/settings/my-data/` }
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
