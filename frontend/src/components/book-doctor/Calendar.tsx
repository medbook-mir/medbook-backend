import React from 'react'
import DateTimePicker from './DateTimePicker'

import { format, addDays } from 'date-fns'

const generateMockData = (): Record<string, string[]> => {
  const times = [
    ['08:30', '15:30'],
    ['09:30', '16:00'],
    ['10:30', '17:30'],
    ['11:30', '18:00'],
    ['12:30'],
    ['13:30'],
    ['14:30']
  ]

  const mock: Record<string, string[]> = {}

  for (let i = 0; i < 7; i++) {
    const date = addDays(new Date(), i)
    const key = format(date, 'yyyy-MM-dd')
    mock[key] = times[i % times.length]
  }

  return mock
}

export const mockData = generateMockData()

export default function BookDoctorCalendar() {
  return (
    <div className="min-h-screen">
      <DateTimePicker timeSlotsByDate={mockData} />
    </div>
  )
}
