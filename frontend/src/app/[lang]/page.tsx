"use client";

import { HeroLeftSide } from "@/components/home/HeroLeftSide";
import HeroSection from "@/components/home/HeroSection";
import { SolutionsSection } from "@/components/home/SolutionsSection";
import { Container } from "@/theme/container";
import { useTranslation } from "react-i18next";

const Home = () => {
  const { t } = useTranslation();

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
