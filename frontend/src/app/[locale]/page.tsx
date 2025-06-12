import HeroSection from "@/components/home/HeroSection";
import HomeBlog from "@/components/home/home-blog";
import MobileApps from "@/components/home/mobile-apps";
import ScheduleInAdvance from "@/components/home/schedule-in-advance";
import { SolutionsSection } from "@/components/home/SolutionsSection";

const Home = () => {
  return (
    <>
      <HeroSection />
      <SolutionsSection />

      {/* Second part of the page */}
      <ScheduleInAdvance />
      <HomeBlog />
      <MobileApps />
    </>
  );
};

export default Home;
