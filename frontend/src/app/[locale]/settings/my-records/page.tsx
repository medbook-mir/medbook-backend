import { useTranslations } from 'next-intl'

const MyRecords = () => {
  const t = useTranslations('settingsLayout.myRecordsPage')

  return <div className="p-10">{t('title')}</div>
}

export default MyRecords
