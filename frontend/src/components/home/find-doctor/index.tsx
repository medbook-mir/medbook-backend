import { images } from '@/assets'
import { Container } from '@/theme/container'
import { CheckIcon } from '@/utils/icons/CheckIcon'
import Image from 'next/image'
import { DoctorCardList } from './available-doctors'
import AnimatedInView from '@/components/shared/animated-in-view'

export const FindDoctor = () => {
  return (
    <Container>
      <div className="relative w-full px-[50px] py-[80px]">
        <AnimatedInView direction="right" variant="slide" delay={0.2}>
          <div className="flex w-[645px] flex-col items-start justify-between gap-[26px]">
            <h1 className="text-[48px] leading-[60px] font-bold text-[#0D0D0D]">
              Find the right doctor according to your complaint
            </h1>
            <p className="w-[530px] text-[14px] leading-[20px] text-[#696969]">
              HealthCare.ly is a free, health app that goes beyond matching you with doctors. It actively helps you find
              the right doctor based on your medical and personal needs and connects you with your HealthCarely
              community for ongoing support throughout your journey to healthier living.
            </p>
            <div>
              <div className="mb-[16px] flex items-center gap-[12px] text-[#121212]">
                <CheckIcon />
                <p>100% free app designed to help you find the right doctor for you.</p>
              </div>
              <div className="flex items-center gap-[12px] text-[#121212]">
                <CheckIcon />
                <p>Available 900 doctors specialist</p>
              </div>
            </div>
            <button className="rounded-[10px] bg-[#046D5F] px-[36px] py-[16px] text-[16px] font-[500] text-white transition hover:bg-gray-200">
              Search the doctor
            </button>
          </div>
        </AnimatedInView>
        <div className="absolute right-0 bottom-0 -mr-4 h-full w-[50%]">
          <AnimatedInView direction="left" variant="slide" delay={0.4}>
            <div className="absolute top-[50px] left-[50px]">
              <DoctorCardList />
            </div>
          </AnimatedInView>
          <Image
            src={images.searchDoctor}
            alt="search doctor image"
            height={600}
            width={700}
            className="right-0 bottom-0 object-contain"
            priority
          />
        </div>
      </div>
    </Container>
  )
}
