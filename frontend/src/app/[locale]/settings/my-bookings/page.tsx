'use client'

import { CustomTabs } from '@/components/ui/tabs'
import { TabsProps } from 'antd'
import { ActiveBookings } from '@/tables/active-bookings'
import { HisotryBookings } from '@/tables/history-bookings'

const MyBookings = () => {
  const items: TabsProps['items'] = [
    {
      key: '1',
      label: 'Active',
      children: <ActiveBookings />
    },
    {
      key: '2',
      label: 'History',
      children: <HisotryBookings />
    }
  ]
  return <CustomTabs panes={items} onChangeTab={() => {}} />
}

export default MyBookings
