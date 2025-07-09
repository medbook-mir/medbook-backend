import { useTranslations } from 'next-intl'
import { Container } from '@/theme/container'
import ResultNumberCard from './card'
import { cardData } from './data'
import AnimatedInView from '@/components/shared/animated-in-view'

const ResultNumbers = () => {
  const t = useTranslations('homePage.resultNumbers')

  return (
    <section className="pt-[264px] pb-[132px]">
      <Container>
        <div className="mx-auto mb-[60px] flex max-w-[750px] flex-col gap-4 text-center">
          <h1 className="text-[46px] leading-[100%] font-bold text-[#0D0D0D]">{t('title')}</h1>
          <p className="text-[20px] leading-7 font-normal text-[#565656]">{t('description')}</p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-8">
          {cardData.map((item, index) => (
            <AnimatedInView direction="up" key={index} variant="slide" delay={index * 0.2}>
              <ResultNumberCard title={item.title} value={item.value} />
            </AnimatedInView>
          ))}
        </div>
      </Container>
    </section>
  )
}
export default ResultNumbers
