import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Container } from '@/theme/container'
import { cardData } from './data'
import AnimatedInView from '@/components/shared/animated-in-view'

const ScheduleInAdvance = () => {
  const t = useTranslations('homePage.scheduleInAdvance')
  return (
    <section className="py-[132px]">
      <Container>
        <div className="mx-auto mb-[60px] flex max-w-[750px] flex-col gap-4 text-center">
          <h1 className="text-[46px] leading-[100%] font-bold text-[#0D0D0D]">
            Make a schedule in advance with the available doctor
          </h1>
          <p className="text-[20px] leading-7 font-normal text-[#565656]">
            Lorem ipsum dolor sit amet consectetur. Orci malesuada mi et mi pellentesque tincidunt at mollis facilisis.
            Nisl eu blandit nunc parturient adipiscing commodo.
          </p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-8">
          {cardData.map((item, index) => (
            <AnimatedInView direction="right" key={index} variant="slide" delay={index * 0.2}>
              <div
                className={`flex w-[352px] gap-8 rounded-[25px] border-[2px] border-[#046D5F80] p-6 ${index === 1 ? 'flex-col-reverse' : 'flex-col'}`}
              >
                <Image src={item.img} alt="Schedule" width={304} height={300} />
                <div className="flex flex-col gap-3">
                  <h3 className="text-[26px] leading-9 font-semibold text-[#0D0D0D]">{item.title}</h3>
                  <p className="text-[16px] leading-6 font-normal text-[#808080]">{item.description}</p>
                </div>
              </div>
            </AnimatedInView>
          ))}
        </div>
      </Container>
    </section>
  )
}
export default ScheduleInAdvance
