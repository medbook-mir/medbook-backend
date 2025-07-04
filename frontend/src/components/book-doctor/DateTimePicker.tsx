'use client'

import React, { useState } from 'react'
import { Card, Button, Typography, Row, Col } from 'antd'
import { LeftOutlined, RightOutlined, CalendarOutlined } from '@ant-design/icons'
import { startOfWeek, addDays, subDays, isSameDay, format } from 'date-fns'

const { Title, Text } = Typography

interface DateTimePickerProps {
  timeSlotsByDate: Record<string, string[]>
}

const DateTimePicker: React.FC<DateTimePickerProps> = ({ timeSlotsByDate }) => {
  const [currentWeekStart, setCurrentWeekStart] = useState<Date>(
    startOfWeek(new Date(), { weekStartsOn: 1 }) // Monday as start of week
  )
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)
  const [selectedTime, setSelectedTime] = useState<string | null>(null)

  const getWeekDates = (): Date[] => {
    return Array.from({ length: 7 }, (_, i) => addDays(currentWeekStart, i))
  }

  const handlePrevWeek = () => {
    setCurrentWeekStart(subDays(currentWeekStart, 7))
  }

  const handleNextWeek = () => {
    setCurrentWeekStart(addDays(currentWeekStart, 7))
  }

  const handleDateClick = (date: Date) => {
    setSelectedDate(date)
    setSelectedTime(null)
  }

  const handleTimeClick = (time: string) => {
    setSelectedTime(time)
  }

  const formattedDate = selectedDate ? format(selectedDate, 'yyyy-MM-dd') : ''
  const timeSlots: string[] = timeSlotsByDate[formattedDate] || []

  return (
    <Card
      style={{
        maxWidth: 790,
        margin: '0 auto',
        boxShadow: '0px 10px 40px 0px #1212121A',
        borderRadius: 16,
        border: 'none',
        padding: 24
      }}
    >
      <Row
        className="direction-col"
        justify="space-between"
        align="middle"
        style={{ marginBottom: 20, paddingBottom: '20px', borderBottom: '1px solid #eee' }}
      >
        <Title level={4} style={{ color: '#046D5F', margin: 0 }}>
          Choose date and time
        </Title>
        <Text>
          <CalendarOutlined /> {format(currentWeekStart, 'MMMM yyyy')}
        </Text>
      </Row>

      <Row justify="space-between" align="middle" style={{ marginBottom: 28 }}>
        <Button icon={<LeftOutlined />} onClick={handlePrevWeek} />
        {getWeekDates().map((date) => (
          <Button
            key={date.toISOString()}
            style={{ width: 58, height: 65, textAlign: 'center', flexDirection: 'column', gap: 0, borderRadius: 8 }}
            type={selectedDate && isSameDay(date, selectedDate) ? 'primary' : 'default'}
            onClick={() => handleDateClick(date)}
          >
            <div style={{ color: '#909090', fontSize: 16 }}>{format(date, 'EEE')}</div>
            <div style={{ fontSize: 20, fontWeight: 700 }}>{format(date, 'd')}</div>
          </Button>
        ))}
        <Button icon={<RightOutlined />} onClick={handleNextWeek} />
      </Row>

      <Row gutter={[8, 8]} style={{ marginBottom: 50, gap: 23 }}>
        {timeSlots.map((time) => (
          <Col key={time}>
            <Button
              type={time === selectedTime ? 'primary' : 'default'}
              onClick={() => handleTimeClick(time)}
              style={{
                padding: '9px 20px',
                borderRadius: 20,
                backgroundColor: time === selectedTime ? '#046D5F' : '#F5F5F5',
                boxShadow: 'none'
              }}
            >
              {time}
            </Button>
          </Col>
        ))}
      </Row>

      {selectedDate && selectedTime && (
        <Row
          justify="space-between"
          align="middle"
          style={{ border: '1px solid #046D5F', backgroundColor: '#F2F7F6', padding: 8, borderRadius: 16 }}
        >
          <Text style={{ fontSize: 16, fontWeight: 500, marginLeft: 8 }}>
            {format(selectedDate, 'd MMMM, yyyy')}
            <span style={{ marginLeft: 12, marginRight: 12 }}>|</span>
            <span style={{ fontWeight: 400 }}>{selectedTime}</span>
          </Text>
          <Button type="primary" style={{ borderRadius: 200, width: 100, fontSize: 14, fontWeight: 400, height: 40 }}>
            Book
          </Button>
        </Row>
      )}
    </Card>
  )
}

export default DateTimePicker
