import HeroSection from '@/components/home/hero'
import HomeBlog from '@/components/home/home-blog'
import MobileApps from '@/components/home/mobile-apps'
import ScheduleInAdvance from '@/components/home/schedule-in-advance'
import { SolutionsSection } from '@/components/home/solutions'
import ResultNumbers from '@/components/home/result-numbers'
import { FindDoctor } from '@/components/home/find-doctor'

const Home = () => {
  return (
    <>
      <HeroSection />
      <SolutionsSection />
      <FindDoctor />
      <ResultNumbers />
      <ScheduleInAdvance />
      <HomeBlog />
      <MobileApps />
    </>
  )
}

export default Home
