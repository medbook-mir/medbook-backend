import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { icons, images } from '@/assets'
import { Link } from '@/i18n/navigation'
import { Container } from '@/theme/container'
import AnimatedInView from '@/components/shared/animated-in-view'

const MobileApps = () => {
  const t = useTranslations('homePage.mobileApps')

  return (
    <section className="bg-[#046D5F] py-20 text-white">
      <Container>
        <div className="flex flex-wrap items-center justify-between gap-12">
          <AnimatedInView direction="right" variant="slide" delay={0.2}>
            <div data-aos="fade-right" className="flex max-w-[570px] flex-col gap-14">
              <div className="flex flex-col gap-5">
                <h2 className="text-[46px] leading-[60px] font-bold">{t('title')}</h2>
                <p className="text-[16px] leading-6 font-normal">{t('description')}</p>
              </div>
              <div className="flex gap-2">
                <Link href="https://play.google.com/store/" target="_blank" rel="noopener noreferrer">
                  <Image src={icons.googlePlay} width={164} height={48} alt="Google play" />
                </Link>
                <Link href="https://apple.com/app-store/" target="_blank" rel="noopener noreferrer">
                  <Image src={icons.appStore} width={164} height={48} alt="App store" />
                </Link>
              </div>
            </div>
          </AnimatedInView>
          <AnimatedInView direction="left" variant="slide" delay={0.4}>
            <div className="flex gap-6">
              <Image src={images.mobileScreenshot1} width={207} alt="Mobile screenshot 1" />
              <Image src={images.mobileScreenshot2} width={207} alt="Mobile screenshot 2" />
            </div>
          </AnimatedInView>
        </div>
      </Container>
    </section>
  )
}
export default MobileApps
