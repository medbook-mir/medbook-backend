import { MainLogoWhite } from '@/utils/icons/MainLogoWhite'
import { Link } from '@/i18n/navigation'
import { Container } from '@/theme/container'
import VerifyForm from '@/forms/verify-form'
import { useTranslations } from 'next-intl'

const Verify = () => {
  const t = useTranslations('verifyPage')

  return (
    <Container>
      <div className="flex h-screen items-center gap-20 py-6">
        <div className="hidden h-full flex-1 flex-col gap-[136px] rounded-4xl bg-[#046D5F] px-10 pt-[70px] lg:flex">
          <Link href="/">
            <MainLogoWhite />
          </Link>
          <div className="flex flex-col gap-11">
            <h2 className="text-[40px] font-medium text-white">{t('title')}</h2>
            <p className="text-[16px] font-medium text-white">{t('description')}</p>
          </div>
        </div>
        <div className="flex-1 px-6 sm:pr-20 sm:pl-12">
          <VerifyForm />
        </div>
      </div>
    </Container>
  )
}

export default Verify
