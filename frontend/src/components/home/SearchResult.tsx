import React, { useEffect, useState } from 'react'
import { Card, Button, Rate, Input, Select, Row, Col, Avatar, Typography, Space, Spin, Empty } from 'antd'
import { EnvironmentOutlined, CheckCircleTwoTone } from '@ant-design/icons'
import { mockDoctors } from '@/utils/helper'

const { Option } = Select
const { Title, Text } = Typography

const DoctorCard = ({ doctor }: { doctor: (typeof mockDoctors)[0] }) => (
  <Card
    key={doctor.id}
    style={{ borderRadius: 12, marginBottom: 24, border: 'none', boxShadow: '0px 10px 40px 0px #1212121A' }}
    bodyStyle={{ padding: 16 }}
  >
    <Row align="middle" style={{ flexWrap: 'nowrap' }} gutter={16}>
      <Col>
        <Avatar shape="square" size={132} style={{ borderRadius: 16 }} src={doctor.avatar} />
      </Col>
      <Col flex="auto">
        <Space direction="vertical" size={4}>
          <Title level={5} style={{ margin: 0, fontWeight: 500, color: '#0D0D0D' }}>
            {doctor.name} <CheckCircleTwoTone twoToneColor="#52c41a" />
          </Title>
          <Text type="secondary" style={{ color: '#046D5F' }}>
            {doctor.specialty}
          </Text>
          <Text>
            <EnvironmentOutlined /> {doctor.location}
          </Text>
          <Rate disabled allowHalf defaultValue={doctor.rating} />
        </Space>
      </Col>
      <Col>
        <Space size={12} direction="vertical">
          <Button type="primary" style={{ borderRadius: 200, width: 120, boxShadow: 'none' }}>
            Book now
          </Button>
          <Button
            style={{
              borderRadius: 200,
              width: '100%',
              maxWidth: 150,
              boxShadow: 'none',
              color: '#046D5F',
              borderColor: '#046D5F'
            }}
          >
            View profile
          </Button>
        </Space>
      </Col>
    </Row>
  </Card>
)

const DoctorSearchResult = ({ searchDoctor }: { searchDoctor: string }) => {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<typeof mockDoctors>([])

  useEffect(() => {
    if (!searchDoctor) {
      setResults([])
      return
    }

    setLoading(true)
    const timeout = setTimeout(() => {
      const filtered = mockDoctors.filter((doc) => doc.name.toLowerCase().includes(searchDoctor.toLowerCase()))
      setResults(filtered)
      setLoading(false)
    }, 1000)

    return () => clearTimeout(timeout)
  }, [searchDoctor])

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: '0 auto' }}>
      <Title level={4} style={{ fontWeight: 500, color: '#0D0D0D', fontSize: 20 }}>
        Search result:
      </Title>

      <Row style={{ marginBottom: 24, width: '100%', gap: 16 }}>
        <Col flex={1.5}>
          <Select placeholder="Language" style={{ width: '100%' }}>
            <Option value="en">English</Option>
            <Option value="uz">Uzbek</Option>
            <Option value="ru">Russian</Option>
          </Select>
        </Col>
        <Col flex={1}>
          <Input placeholder="Text" style={{ width: '100%' }} />
        </Col>
      </Row>

      {loading ? (
        <Spin style={{ margin: '0 auto', display: 'block' }} tip="Loading doctors..." />
      ) : results.length > 0 ? (
        results.map((doctor) => <DoctorCard key={doctor.id} doctor={doctor} />)
      ) : searchDoctor ? (
        <Empty description="No doctors found" />
      ) : null}
    </div>
  )
}

export default DoctorSearchResult
