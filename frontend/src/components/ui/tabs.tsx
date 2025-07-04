'use client'

import { useState } from 'react'
import { Tabs, TabsProps } from 'antd'
import styled from 'styled-components'

type CustomTabsProps = {
  panes: TabsProps['items']
  onChangeTab: (key: string) => void
} & TabsProps

export const CustomTabs = ({ panes, onChangeTab, ...props }: CustomTabsProps) => {
  const initialActiveKey = panes ? panes[0].key : ''
  const [activeKey, setActiveKey] = useState(initialActiveKey)

  const handleTabClick = (key: string) => {
    setActiveKey(key)
    onChangeTab(key)
  }

  return (
    <StyledTabs
      activeKey={activeKey}
      renderTabBar={() => (
        <div className="flex gap-8 border-b-2 border-[#E9ECF4]">
          {panes?.map((pane) => (
            <div
              key={pane.key}
              className={`cursor-pointer border-b-4 px-8 py-[18px] text-[16px] leading-6 font-semibold transition-colors duration-300 ${pane.key === activeKey ? 'border-[#264796] text-[#000]' : 'border-transparent text-[#797979]'} `}
              onClick={() => handleTabClick(pane.key)}
            >
              {pane.label}
            </div>
          ))}
        </div>
      )}
      {...props}
      items={panes}
    />
  )
}

const StyledTabs = styled(Tabs)`
  border-left: 0 !important;
  .ant-tabs-tabpane > div {
    padding: 0 !important;
  }
`
