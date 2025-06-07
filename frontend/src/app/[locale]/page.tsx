import HeroSection from "@/components/home/HeroSection";
import { SolutionsSection } from "@/components/home/SolutionsSection";
import { Container } from "@/theme/container";

const Home = () => {
  return (
    <div className="py-8">
      <Container>
        <HeroSection />
        <SolutionsSection />
      </Container>
    </div>
  );
};

export default Home;
