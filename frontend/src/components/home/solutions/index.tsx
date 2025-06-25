import { Container } from '@/theme/container'
import { solutionsSteps, solutionsTitle } from './data'

export const SolutionsSection = () => {
  return (
    <section className="px-[104px] py-[132px]">
      <Container>
        <h2 className="mb-[60px] text-center text-[48px] leading-[60px] font-bold tracking-[-2%] text-[#0D0D0D]">
          {solutionsTitle}
        </h2>
        <div className="mx-auto grid gap-[17px] sm:grid-cols-2 lg:grid-cols-4">
          {solutionsSteps.map((step, index) => (
            <div
              data-aos="fade-left"
              key={index}
              className="flex h-[226px] w-full flex-col justify-center rounded-b-[10px] border-t-[3px] border-[#046D5F] bg-white px-[24px] shadow-[0px_10px_40px_0px_#1212121A] transition-shadow hover:shadow-lg"
            >
              <div className="mb-4">{step.icon}</div>
              <h3 className="mb-2 text-[14px] leading-[28px] font-bold tracking-[3%]">{step.title}</h3>
              <p className="text-[12px] text-[#696969]">{step.description}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  )
}
