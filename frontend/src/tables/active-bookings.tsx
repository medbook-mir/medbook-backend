'use client'

import { TableProps } from 'antd'
import { CustomTable } from '../components/ui/table'
import { Link } from '@/i18n/navigation'
import { useTranslations } from 'next-intl'

export const ActiveBookings = () => {
  const t = useTranslations('settingsLayout.myBookingsPage')

  const getColumns: TableProps<any>['columns'] = [
    {
      key: 'orderNumber',
      dataIndex: 'orderNumber',
      title: t('orderNumber'),
      width: 330,
      render: (value: string) => <p className="typography-h5 font-bold">{value}</p>
    },
    {
      key: 'date',
      dataIndex: 'date',
      title: t('date'),
      width: 300,
      render: (value: string) => <p className="typography-h5 font-bold">{value}</p>
    },
    {
      key: 'appointmentType',
      dataIndex: 'appointmentType',
      title: t('appointmentType'),
      width: 300,
      render: (value: string) => <p className="typography-h5 font-bold">{t(value)}</p>
    },
    {
      key: 'status',
      dataIndex: 'status',
      title: t('status'),
      width: 150,
      render: (value: string) => <p className="typography-body font-bold">{t(value)}</p>
    },
    {
      key: 'doctor',
      dataIndex: 'doctor',
      title: t('doctor'),
      width: 150,
      render: ({ name, id, orientation }: { name: string; id: string; orientation: string }) => (
        <div className="typography-body font-bold">
          <Link href={`/doctors/${id}`}>{name}</Link>
          <p className="typography-body font-bold">{orientation}</p>
        </div>
      )
    }
  ]

  return <CustomTable dataSource={[]} columns={getColumns} />
}
