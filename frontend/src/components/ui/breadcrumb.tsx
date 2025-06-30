'use client'

import { cn } from '@/utils/helper'
import { Breadcrumb } from 'antd'
import { HomeOutlined } from '@ant-design/icons'
import { useTranslations } from 'next-intl'
import { usePathname } from '@/i18n/navigation'

type CustomBreadcrumbProps = {
  className?: string
  pages: {
    title: string
    href: string
  }[]
}

export const CustomBreadcrumb = ({ className, pages, ...props }: CustomBreadcrumbProps) => {
  const t = useTranslations()
  const pathname = usePathname()

  return (
    <Breadcrumb
      {...props}
      className={cn('flex items-center px-4 lg:px-0', className)}
      separator="/"
      items={[
        {
          title: (
            <span className="inline-flex items-center gap-2">
              <HomeOutlined />
              <span>{t('homePage.home')}</span>
            </span>
          ),
          href: '/'
        },
        ...pages.map((page) => ({
          title: <span className={pathname === page.href ? 'font-medium' : ''}>{page.title}</span>,
          href: page.href
        }))
      ]}
    />
  )
}
