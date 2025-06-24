import HeroSection from '@/components/home/hero'
import HomeBlog from '@/components/home/home-blog'
import MobileApps from '@/components/home/mobile-apps'
import ScheduleInAdvance from '@/components/home/schedule-in-advance'
import { SolutionsSection } from '@/components/home/solutions'
import { Container } from '@/theme/container'
import Header from '@/components/header'
import ResultNumbers from '@/components/home/result-numbers'
import { FindDoctor } from '@/components/home/find-doctor'

const Home = () => {
  return (
    <div>
      {/* <Container> */}
      <div className="relative rounded-b-[35px] bg-[#046D5F] px-[80px] py-[52px]">
        <Header />
        <HeroSection />
      </div>
      {/* </Container> */}
      <SolutionsSection />
      <FindDoctor />
      <ResultNumbers />
      <ScheduleInAdvance />
      <HomeBlog />
      <MobileApps />
    </div>
  )
}

export default Home
