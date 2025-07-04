'use client'

import { useTranslations } from 'next-intl'
import { LocationIcon } from '@/utils/icons/LocationIcon'
import { SearchIcon } from '@/utils/icons/SearchIcon'

export const HeroLeftSide = () => {
  const t = useTranslations('homePage.hero')

  return (
    <div className="flex flex-col gap-6">
      <div className="space-y-4">
        <h1 className="typography-h2bold text-primary">{t('title')}</h1>
        <p className="typography-body-xl text-gray">{t('description')}</p>
      </div>

      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-4">
          <SearchIcon />
          <input
            type="text"
            placeholder={t('search_placeholder')}
            className="placeholder:text-gray flex-1 border-none bg-transparent outline-none"
          />
        </div>

        <div className="text-gray flex items-center gap-2">
          <LocationIcon />
          <span className="typography-body">{t('location')}</span>
        </div>
      </div>
    </div>
  )
}
