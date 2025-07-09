'use client'

import { CustomTabs } from '@/components/ui/tabs'
import { TabsProps } from 'antd'
import { ActiveBookings } from '@/tables/active-bookings'
import { HisotryBookings } from '@/tables/history-bookings'
import { useTranslations } from 'next-intl'

const MyBookings = () => {
  const t = useTranslations('settingsLayout.myBookingsPage')

  const items: TabsProps['items'] = [
    {
      key: '1',
      label: t('active'),
      children: <ActiveBookings />
    },
    {
      key: '2',
      label: t('history'),
      children: <HisotryBookings />
    }
  ]
  return <CustomTabs panes={items} onChangeTab={() => {}} />
}

export default MyBookings
