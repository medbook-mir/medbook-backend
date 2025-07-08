import { useTranslations } from 'next-intl'

const Payment = () => {
  const t = useTranslations('settingsLayout.paymentPage')

  return <div className="p-10">{t('title')}</div>
}

export default Payment
