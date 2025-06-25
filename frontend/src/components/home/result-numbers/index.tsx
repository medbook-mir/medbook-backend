import { Container } from '@/theme/container'
import { cardData } from './data'
import ResultNumberCard from './card'

const ResultNumbers = () => {
  return (
    <section className="pt-[264px] pb-[132px]">
      <Container>
        <div className="mx-auto mb-[60px] flex max-w-[750px] flex-col gap-4 text-center">
          <h1 className="text-[46px] leading-[100%] font-bold text-[#0D0D0D]">
            We’re employee benefit at  7500+ hospital
          </h1>
          <p className="text-[20px] leading-7 font-normal text-[#565656]">
            Effective progress tracking and milestone setting are critical components of any successful project or
            personal goal. By systematically monitoring our achievements.
          </p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-8">
          {cardData.map((item, index) => (
            <ResultNumberCard key={index} title={item.title} value={item.value} />
          ))}
        </div>
      </Container>
    </section>
  )
}
export default ResultNumbers
