'use client'

import { useParams, usePathname } from 'next/navigation'
import styled from 'styled-components'
import { CustomSelect } from '@/components/ui/select'
import { useRouter } from '@/i18n/navigation'
import { routing, Locale } from '@/i18n/routing'
import { WorldIcon } from '@/utils/icons'

const langOptions = [
  { label: 'Eng', value: 'en' },
  { label: 'Uzb', value: 'uz' },
  { label: 'Ўзб', value: 'oz' },
  { label: 'Рус', value: 'ru' }
]

const renderLangOptions = langOptions.map((option) => ({
  label: <div className="flex w-full justify-center">{option.label}</div>,
  value: option.value
}))

const StyledLangSelect = styled(CustomSelect)`
  width: 100px;
  font-weight: 400 !important;
  font-size: 14px !important;
  line-height: 14px !important;
  height: 40px !important;

  .ant-select-item-option-selected {
    background-color: #fafafa !important;
  }

  .ant-select-item {
    font-weight: 400 !important;
    font-size: 14px !important;
    line-height: 14px !important;
    text-align: center !important;
    color: #046d5f;
  }

  .ant-select-item:hover {
    background-color: #f5f5f5 !important;
  }
  .ant-select-selector {
    border: 1px solid #fff !important;
    border-radius: 62px !important;
    background-color: transparent !important;
    display: flex !important;
    align-items: center !important;
  }

  /* Selected item text color (button) */
  .ant-select-selection-item {
    color: #fff !important;
    flex-grow: 1;
    text-align: center;
    overflow: visible !important;
    padding-right: 0 !important;
    padding-left: 4px !important;
  }

  /* Arrow icon */
  .ant-select-arrow {
    display: inline-block !important;
    color: #fff !important;
    right: 16px !important;
  }
`

export const LangSelect = () => {
  const { locale } = useParams<{ locale: Locale }>()
  const pathname = usePathname()
  const router = useRouter()

  const handleLangChange = (value: Locale) => {
    if (!routing.locales.includes(value)) {
      console.error(`Invalid locale: ${value}`)
      return
    }
    try {
      // Get the current path without the locale prefix
      const pathWithoutLocale = pathname.replace(`/${locale}`, '') || '/'
      router.replace(pathWithoutLocale, { locale: value })
      localStorage.setItem('language', value)
    } catch (error) {
      console.error('Failed to change language:', error)
    }
  }

  return (
    <div className="relative flex items-center">
      <span className="pointer-events-none absolute left-4 z-[1]">
        <WorldIcon />
      </span>
      <StyledLangSelect value={locale} options={renderLangOptions} onSelect={handleLangChange} />
    </div>
  )
}
