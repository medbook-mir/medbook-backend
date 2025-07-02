import { Table, TableProps } from 'antd'
import styled from 'styled-components'

type CustomTableProps<T> = {
  dataSource: T[]
  rowKey?: string
  columns: TableProps<T>['columns']
  classes?: string
  rowClassName?: 'success' | 'warning' | 'error'
  singleRowClassName?: (record: T) => string
}

interface TableRecord {
  statusKey?: string
  key: string
  desc?: string
}

export const CustomTable = <T extends TableRecord>({
  dataSource,
  columns,
  classes,
  rowKey,
  rowClassName,
  singleRowClassName,
  ...props
}: CustomTableProps<T> & TableProps<T>) => {
  return (
    <div className="relative px-4 py-5 lg:px-0">
      <StyledTable
        {...({
          bordered: false,
          className: `custom-table ${classes}`,
          dataSource,
          columns,
          pagination: false,
          rowKey: (record: any) => String(record.key),
          loading: false,
          rowClassName: (record: any) =>
            `cursor-pointer ${rowClassName ? rowClassName : ''} ${singleRowClassName ? singleRowClassName(record) : ''}`,
          ...props
        } as any)}
      />
    </div>
  )
}

const StyledTable = styled(Table)`
  .ant-table-thead {
    tr {
      th {
        background: transparent;
        padding-top: 24px;
        padding-bottom: 24px;
        font-weight: 500;
        color: #797979;
        font-size: 14px;
        line-height: 18px;
        text-transform: uppercase;
      }
    }
  }
  .ant-table-tbody {
    tr {
      td {
        padding-top: 12px;
        padding-bottom: 12px;
        font-weight: 400;
        color: #000;
        font-size: 14px;
        line-height: 20px;
      }
    }
  }
`
