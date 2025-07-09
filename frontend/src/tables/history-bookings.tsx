'use client'

import { TableProps } from 'antd'
import { CustomTable } from '../components/ui/table'
import { Link } from '@/i18n/navigation'
import { Status } from '@/components/ui/status'
import { useTranslations } from 'next-intl'

const mockData = [
  {
    orderNumber: '1231235',
    date: '20.02.2025',
    appointmentType: 'Online',
    status: 'canceled',
    doctor: {
      name: 'Kathrin Schenk-Losse',
      id: '1',
      orientation: 'Gynecologist'
    }
  },
  {
    orderNumber: '6589740',
    date: '20.02.2025',
    appointmentType: 'Offline',
    status: 'canceled',
    doctor: {
      name: 'Kathrin Schenk-Losse',
      id: '1',
      orientation: 'Gynecologist'
    }
  },
  {
    orderNumber: '4569871',
    date: '20.02.2025',
    appointmentType: 'Online',
    status: 'success',
    doctor: {
      name: 'Kathrin Schenk-Losse',
      id: '1',
      orientation: 'Gynecologist'
    }
  }
]

export const HisotryBookings = () => {
  const t = useTranslations('settingsLayout.myBookingsPage')

  const getColumns: TableProps<any>['columns'] = [
    {
      key: 'orderNumber',
      dataIndex: 'orderNumber',
      title: t('orderNumber'),
      width: 180,
      render: (value: string) => <p>#{value}</p>
    },
    {
      key: 'date',
      dataIndex: 'date',
      title: t('date'),
      width: 180,
      render: (value: string) => <p>{value}</p>
    },
    {
      key: 'appointmentType',
      dataIndex: 'appointmentType',
      title: t('appointmentType'),
      width: 160,
      render: (value: string) => <p>{value}</p>
    },
    {
      key: 'status',
      dataIndex: 'status',
      title: t('status'),
      width: 180,
      render: (value: 'canceled' | 'success') => <Status status={value} />
    },
    {
      key: 'doctor',
      dataIndex: 'doctor',
      title: t('doctor'),
      width: 360,
      render: ({ name, id, orientation }: { name: string; id: string; orientation: string }) => (
        <div>
          <Link className="text-[#1F88E4] !underline underline-offset-2" href={`/doctors/${id}`}>
            {name}
          </Link>
          <p>{orientation}</p>
        </div>
      )
    }
  ]

  const dataWithKey = mockData.map((item) => ({ ...item, key: item.orderNumber }))

  return <CustomTable dataSource={dataWithKey} columns={getColumns} />
}
