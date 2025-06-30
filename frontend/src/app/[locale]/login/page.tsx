import { useTranslations } from 'next-intl'
import { MainLogoWhite } from '@/assets/icons/MainLogoWhite'
import LoginForm from '@/forms/login-form'
import { Link } from '@/i18n/navigation'
import { Container } from '@/theme/container'

const Login = () => {
  const t = useTranslations('loginPage')
  return (
    <Container>
      <div className="flex h-screen items-center gap-20 py-6">
        <div className="flex h-full flex-1 flex-col gap-[136px] rounded-4xl bg-[#046D5F] px-10 pt-[70px]">
          <Link href="/">
            <MainLogoWhite />
          </Link>
          <div className="flex flex-col gap-11">
            <h2 className="text-[40px] font-medium text-white">{t('title')}</h2>
            <p className="text-[16px] font-medium text-white">{t('description')}</p>
          </div>
        </div>
        <LoginForm />
      </div>
    </Container>
  )
}

export default Login
