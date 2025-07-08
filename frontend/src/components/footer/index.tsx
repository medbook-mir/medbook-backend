import { useTranslations } from 'next-intl'
import { images } from '@/assets'
import { Link } from '@/i18n/navigation'
import { Container } from '@/theme/container'
import Image from 'next/image'
import { footerLinks, footerSocials } from './data'

const Footer = () => {
  const t = useTranslations('homePage.footer')

  return (
    <footer>
      <Container>
        <div className="flex flex-wrap items-center justify-center gap-12 py-[70px] sm:justify-between">
          <div className="flex max-w-[267px] flex-col gap-4">
            <Link href="#">
              <Image src={images.footerLogo} width={168} alt="Footer logo" />
            </Link>
            <p className="text-[16px] leading-6 font-normal text-[#808080]">{t('description')}</p>
          </div>
          <div className="flex flex-wrap gap-[100px]">
            <div className="flex flex-col gap-4">
              {footerLinks.map((item, index) => (
                <Link key={index} href={item.href} className="text-[16px] leading-6 font-normal text-[#808080]">
                  {t(item.title)}
                </Link>
              ))}
            </div>
            <div className="flex flex-col gap-4">
              {footerLinks.map((item, index) => (
                <Link key={index} href={item.href} className="text-[16px] leading-6 font-normal text-[#808080]">
                  {t(item.title)}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-3.5">
            {footerSocials.map((item, index) => (
              <Link key={index} href={item.href} target="_blank" rel="noopener noreferrer">
                <item.icon />
              </Link>
            ))}
          </div>
        </div>
        <div className="flex flex-wrap justify-between gap-6 border-t border-t-[#D6D6D6] py-6 text-[16px] leading-7 font-normal text-[#0D0D0D]">
          <p>{t('copyright')}</p>
          <div className="flex flex-wrap gap-x-12 gap-y-2">
            <p>{t('customerService')}</p>
            <p>{t('termsConditions')}</p>
            <p>{t('privacyPolicy')}</p>
          </div>
        </div>
      </Container>
    </footer>
  )
}

export default Footer
