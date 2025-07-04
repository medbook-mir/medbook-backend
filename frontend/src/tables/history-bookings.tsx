import { TableProps } from 'antd'
import { CustomTable } from '../components/ui/table'
import { Link } from '@/i18n/navigation'
import { Status } from '@/components/ui/status'

const mockData = [
  {
    orderNumber: '1231235',
    date: '20.02.2025',
    appointmentType: 'Online',
    status: 'CANCELED',
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
    status: 'CANCELED',
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
    status: 'SUCCESS',
    doctor: {
      name: 'Kathrin Schenk-Losse',
      id: '1',
      orientation: 'Gynecologist'
    }
  }
]

export const HisotryBookings = () => {
  const getColumns: TableProps<any>['columns'] & { key: string }[] = [
    {
      key: 'orderNumber',
      dataIndex: 'orderNumber',
      title: 'Order number',
      width: 160,
      render: (value: string) => <p>#{value}</p>
    },
    {
      key: 'date',
      dataIndex: 'date',
      title: 'Date',
      width: 160,
      render: (value: string) => <p>{value}</p>
    },
    {
      key: 'appointmentType',
      dataIndex: 'appointmentType',
      title: 'Appointment type',
      width: 160,
      render: (value: string) => <p>{value}</p>
    },
    {
      key: 'status',
      dataIndex: 'status',
      title: 'Status',
      width: 160,
      render: (value: 'CANCELED' | 'SUCCESS') => <Status status={value} />
    },
    {
      key: 'doctor',
      dataIndex: 'doctor',
      title: 'Doctor',
      width: 400,
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
