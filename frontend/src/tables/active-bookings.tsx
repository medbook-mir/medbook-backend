import { TableProps } from 'antd'
import { CustomTable } from '../components/ui/table'
import { Link } from '@/i18n/navigation'

export const ActiveBookings = () => {
  const getColumns: TableProps<any>['columns'] & { key: string }[] = [
    {
      key: 'orderNumber',
      dataIndex: 'orderNumber',
      title: 'ORDER NUMBER',
      width: 330,
      render: (value: string) => <p className="typography-h5 font-bold">{value}</p>
    },
    {
      key: 'date',
      dataIndex: 'date',
      title: 'DATE',
      width: 300,
      render: (value: string) => <p className="typography-h5 font-bold">{value}</p>
    },
    {
      key: 'appointmentType',
      dataIndex: 'appointmentType',
      title: 'APPOINTMENT TYPE',
      width: 300,
      render: (value: string) => <p className="typography-h5 font-bold">{value}</p>
    },
    {
      key: 'status',
      dataIndex: 'status',
      title: 'STATUS',
      width: 150,
      render: (value: string) => <p className="typography-body font-bold">{value}</p>
    },
    {
      key: 'doctor',
      dataIndex: 'doctor',
      title: 'DOCTOR',
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
