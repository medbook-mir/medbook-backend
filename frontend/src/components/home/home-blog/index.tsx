import { useTranslations } from 'next-intl'
import Image from 'next/image'
import { Container } from '@/theme/container'
import { cardData } from './data'
import { Link } from '@/i18n/navigation'
import { RightRedIcon } from '@/utils/icons/arrow-icons'
import AnimatedInView from '@/components/shared/animated-in-view'

const HomeBlog = () => {
  const t = useTranslations('homePage.blog')

  return (
    <section className="py-20">
      <Container>
        <div className="mx-auto mb-[60px] flex max-w-[750px] flex-col gap-4 text-center">
          <h1 className="text-[46px] leading-[100%] font-bold text-[#0D0D0D]">{t('title')}</h1>
          <p className="text-[20px] leading-7 font-normal text-[#565656]">{t('description')}</p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-8">
          {cardData.map((item, index) => (
            <AnimatedInView direction="down" key={index} variant="slide" delay={index * 0.2}>
              <div className="flex w-[384px] flex-col gap-8 rounded-[25px] border-[2px] border-[#B5B5B580] p-6">
                <Image src={item.img} alt="Schedule" width={304} />
                <div className="flex flex-col gap-5">
                  <div className="flex flex-col gap-3">
                    <h3 className="text-[16px] leading-[26px] font-bold text-[#222]">{item.title}</h3>
                    <p className="text-[12px] leading-4 font-medium text-[#555]">{item.description}</p>
                  </div>
                  <div className="flex items-center justify-between">
                    <Link href={item.link} className="flex cursor-pointer items-center gap-3">
                      <span className="text-[14px] leading-6 font-medium underline">Learn more</span>
                      <RightRedIcon />
                    </Link>
                    <p className="text-[14px] leading-6 font-normal text-[#555]">{item.date}</p>
                  </div>
                </div>
              </div>
            </AnimatedInView>
          ))}
        </div>
      </Container>
    </section>
  )
}

export default HomeBlog
