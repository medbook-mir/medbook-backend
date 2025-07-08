import { forwardRef } from 'react'
import { DatePicker } from 'antd'
import type { DatePickerProps } from 'antd'
import styled from 'styled-components'
import { cn } from '@/utils/helper'

type DatepickerInputProps = DatePickerProps & {
  status?: 'error' | 'warning' | ''
}

const DatepickerInput = forwardRef<any, DatepickerInputProps>(
  ({ placeholder, className, disabled, status, ...props }, ref) => {
    return (
      <StyledDatePicker
        {...props}
        status={status}
        ref={ref}
        placeholder={placeholder}
        disabled={disabled}
        className={cn('w-full', className)}
      />
    )
  }
)

DatepickerInput.displayName = 'DatepickerInput'

const StyledDatePicker = styled(DatePicker)<DatepickerInputProps>`
  background-color: #f7f7f7 !important;
  padding: 8px 16px !important;
  color: #0d0d0d !important;
  ::placeholder {
    color: #696969 !important;
  }
  .ant-input {
    &:disabled {
      color: #000 !important;
    }
  }
`

export default DatepickerInput
